import torch
from torch.utils.data import DataLoader
import numpy as np
import pandas as pd
from peft import LoraConfig, get_peft_model
from peft.utils.other import fsdp_auto_wrap_policy
from transformers import EsmForMaskedLM, EsmTokenizer
import os
from accelerate import Accelerator

from data_utils import Mutation_Set, split_train, sample_data
from stat_utils import spearman, compute_score, BT_loss, KLloss
from inference import Inference
from common import stub,image
import warnings
warnings.filterwarnings("ignore")


def train(model, model_reg, trainloder, optimizer, tokenizer, lambda_reg):

    model.train()

    total_loss = 0.

    for step, data in enumerate(trainloder):
        seq, mask = data[0], data[1]
        wt, wt_mask = data[2], data[3]
        pos = data[4]
        golden_score = data[5]
        score, logits = compute_score(model, seq, mask, wt, pos, tokenizer)
        score = score.cuda()

        l_BT = BT_loss(score, golden_score)

        out_reg = model_reg(wt, wt_mask)
        logits_reg = out_reg.logits
        l_reg = KLloss(logits, logits_reg, seq, mask)

        loss = l_BT + lambda_reg*l_reg

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    return total_loss


def evaluate(model, testloader, tokenizer, accelerator, istest=False):
    model.eval()
    seq_list = []
    score_list = []
    gscore_list = []
    with torch.no_grad():
        for step, data in enumerate(testloader):
            seq, mask = data[0], data[1]
            wt, wt_mask = data[2], data[3]
            pos = data[4]
            golden_score = data[5]
            pid = data[6]
            if istest:
                pid = pid.cuda()
                pid = accelerator.gather(pid)
                for s in pid:
                    seq_list.append(s.cpu())

            score, logits = compute_score(model, seq, mask, wt, pos, tokenizer)

            score = score.cuda()
            score = accelerator.gather(score)
            golden_score = accelerator.gather(golden_score)
            score = np.asarray(score.cpu())
            golden_score = np.asarray(golden_score.cpu())
            score_list.extend(score)
            gscore_list.extend(golden_score)
    score_list = np.asarray(score_list)
    gscore_list = np.asarray(gscore_list)
    sr = spearman(score_list, gscore_list)

    if istest:
        seq_list = np.asarray(seq_list)

        return sr, score_list, seq_list
    else:
        return sr


def train_confit(
    dataset,
    model_name='ESM-1v',
    model_seed=1,
    sample_seed=0,
    shot=48,
    batch_size=16,
    max_epochs=30,
    ini_lr=5e-4,
    min_lr=1e-4,
    endure_time=5,
    lambda_reg=0.1,
    lora_r=8,
    lora_alpha=8,
    lora_dropout=0.1,
    checkpoint_dir='checkpoint',
    predicted_dir='predicted',
    no_retrieval=False,
    retrieval_alpha=0.8
):
    accelerator = Accelerator()

    # Create model
    if model_name == 'ESM-1v':
        basemodel = EsmForMaskedLM.from_pretrained(
            f'facebook/esm1v_t33_650M_UR90S_{model_seed}')
        model_reg = EsmForMaskedLM.from_pretrained(
            f'facebook/esm1v_t33_650M_UR90S_{model_seed}')
        tokenizer = EsmTokenizer.from_pretrained(
            f'facebook/esm1v_t33_650M_UR90S_{model_seed}')
    elif model_name == 'ESM-2':
        basemodel = EsmForMaskedLM.from_pretrained(
            'facebook/esm2_t48_15B_UR50D')
        model_reg = EsmForMaskedLM.from_pretrained(
            'facebook/esm2_t48_15B_UR50D')
        tokenizer = EsmTokenizer.from_pretrained('facebook/esm2_t48_15B_UR50D')
    elif model_name == 'ESM-1b':
        basemodel = EsmForMaskedLM.from_pretrained(
            'facebook/esm1b_t33_650M_UR50S')
        model_reg = EsmForMaskedLM.from_pretrained(
            'facebook/esm1b_t33_650M_UR50S')
        tokenizer = EsmTokenizer.from_pretrained(
            'facebook/esm1b_t33_650M_UR50S')

    for pm in model_reg.parameters():
        pm.requires_grad = False
    model_reg.eval()    # Regularization model

    peft_config = LoraConfig(
        task_type="CAUSAL_LM",
        r=lora_r,
        lora_alpha=lora_alpha,
        lora_dropout=lora_dropout,
        target_modules=["query", "value"]
    )

    model = get_peft_model(basemodel, peft_config)

    # Create optimizer and scheduler
    optimizer = torch.optim.Adam(model.parameters(), lr=ini_lr)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingWarmRestarts(
        optimizer, T_0=2*max_epochs, eta_min=min_lr)
    if os.environ.get("ACCELERATE_USE_FSDP", None) is not None:
        accelerator.state.fsdp_plugin.auto_wrap_policy = fsdp_auto_wrap_policy(
            model)
    model, optimizer, scheduler = accelerator.prepare(
        model, optimizer, scheduler)
    model_reg = accelerator.prepare(model_reg)

    accelerator.print(
        f'===================dataset:{dataset}, preparing data=============')

    # Sample data
    if accelerator.is_main_process:
        sample_data(dataset, sample_seed, shot)
        split_train(dataset)

    with accelerator.main_process_first():
        train_csv = pd.DataFrame(None)
        test_csv = pd.read_csv(f'data/{dataset}/test.csv')
        for i in range(1, 6):
            if i == model_seed:
                # Using 1/5 train data as validation set
                val_csv = pd.read_csv(f'data/{dataset}/train_{i}.csv')
            temp_csv = pd.read_csv(f'data/{dataset}/train_{i}.csv')
            train_csv = pd.concat([train_csv, temp_csv], axis=0)

    # Create dataset and dataloader
    trainset = Mutation_Set(data=train_csv, fname=dataset, tokenizer=tokenizer)
    testset = Mutation_Set(data=test_csv, fname=dataset,  tokenizer=tokenizer)
    valset = Mutation_Set(data=val_csv, fname=dataset,  tokenizer=tokenizer)
    with accelerator.main_process_first():
        trainloader = DataLoader(
            trainset, batch_size=batch_size, collate_fn=trainset.collate_fn, shuffle=True)
        testloader = DataLoader(testset, batch_size=2,
                                collate_fn=testset.collate_fn)
        valloader = DataLoader(valset, batch_size=2,
                               collate_fn=testset.collate_fn)

    trainloader = accelerator.prepare(trainloader)
    testloader = accelerator.prepare(testloader)
    valloader = accelerator.prepare(valloader)
    accelerator.print('==============data preparing done!================')

    best_sr = -np.inf
    endure = 0

    for epoch in range(max_epochs):
        loss = train(model, model_reg, trainloader,
                     optimizer, tokenizer, lambda_reg)
        accelerator.print(
            f'========epoch{epoch}; training loss :{loss}=================')
        sr = evaluate(model, valloader, tokenizer, accelerator)
        accelerator.print(
            f'========epoch{epoch}; val spearman correlation :{sr}=================')
        scheduler.step()
        if best_sr > sr:
            endure += 1
        else:
            endure = 0
            best_sr = sr

            if not os.path.isdir(os.path.join(checkpoint_dir, dataset)):
                if accelerator.is_main_process:
                    os.makedirs(os.path.join(checkpoint_dir, dataset))
            save_path = os.path.join(
                checkpoint_dir, dataset, f'seed{model_seed}')
            accelerator.wait_for_everyone()
            unwrapped_model = accelerator.unwrap_model(model)
            unwrapped_model.save_pretrained(save_path)
        if sr == 1.0:
            accelerator.print(
                f'========early stop at epoch{epoch}!============')
            break
        if endure > endure_time:
            accelerator.print(
                f'========early stop at epoch{epoch}!============')
            break

    # Inference on the test set
    accelerator.print('=======training done!, test the performance!========')
    inference = Inference(
        dataset=dataset,
        checkpoint_dir=checkpoint_dir,
        predicted_dir=predicted_dir,
        model_name=model_name,
        model_seed=model_seed,
        no_retrieval=no_retrieval,
        retrieval_alpha=retrieval_alpha
    )
    sr, score, pid = inference.evaluate(testloader)
    inference.save_prediction(score, pid)
    inference.save_summary(sr, shot)
    accelerator.print(
        f'=============the test spearman correlation for early stop: {sr}==================')

@stub.local_entrypoint()

