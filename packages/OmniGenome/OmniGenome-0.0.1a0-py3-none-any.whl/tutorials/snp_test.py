# -*- coding: utf-8 -*-
# file: snp_test.py
# time: 14:22 06/04/2024
# author: YANG, HENG <hy345@exeter.ac.uk> (杨恒)
# github: https://github.com/yangheng95
# huggingface: https://huggingface.co/yangheng
# google scholar: https://scholar.google.com/citations?user=NPq5a_0AAAAJ&hl=en
# Copyright (C) 2019-2024. All Rights Reserved.

import torch
from transformers import AutoModel, AutoConfig

from omnigenome.src.dataset.omnigenome_dataset import (
    OmniGenomeDatasetForTokenRegression,
)
from omnigenome.src.metric.classification_metric import ClassificationMetric
from omnigenome.src.metric.regression_metric import RegressionMetric
from omnigenome.src.misc.utils import seed_everything
from omnigenome.src.tokenizer.single_nucleotide_tokenizer import (
    OmniSingleNucleotideTokenizer,
)
from omnigenome.src.model.regression.model import (
    OmniGenomeEncoderModelForTokenRegression,
)
from omnigenome.src.trainer.trainer import Trainer


label2id = {"(": 0, ")": 1, ".": 2}

model_name_or_path = "pretrained_models/mprna_small_new"
# model_name_or_path = "pretrained_models/mprna_base_new"
SN_tokenizer = OmniSingleNucleotideTokenizer.from_pretrained(model_name_or_path)

config = AutoConfig.from_pretrained(
    model_name_or_path, num_labels=1, trust_remote_code=True
)

model = OmniGenomeEncoderModelForTokenRegression(
    config, model_name_or_path, tokenizer=SN_tokenizer, trust_remote_code=True
)

# epochs = 20
epochs = 1
learning_rate = 2e-5
weight_decay = 1e-5
batch_size = 8
seeds = [42]
# seeds = [45, 46, 47]


# epochs = 10
epochs = 1
learning_rate = 2e-5
weight_decay = 1e-5
batch_size = 8
seeds = [42]
# seeds = [45, 46, 47]

train_file = "benchmark/hgb_datasets/RNA-SNPP/train.json"
test_file = "benchmark/hgb_datasets/RNA-SNPP/test.json"
valid_file = "benchmark/hgb_datasets/RNA-SNPP/valid.json"

train_set = OmniGenomeDatasetForTokenRegression(
    data_source=train_file,
    tokenizer=SN_tokenizer,
    max_length=210,
)
test_set = OmniGenomeDatasetForTokenRegression(
    data_source=test_file,
    tokenizer=SN_tokenizer,
    max_length=210,
)
valid_set = OmniGenomeDatasetForTokenRegression(
    data_source=valid_file,
    tokenizer=SN_tokenizer,
    max_length=210,
)
train_loader = torch.utils.data.DataLoader(
    train_set, batch_size=batch_size, shuffle=True
)
valid_loader = torch.utils.data.DataLoader(valid_set, batch_size=batch_size)
test_loader = torch.utils.data.DataLoader(test_set, batch_size=batch_size)

# compute_metrics = ClassificationMetric(ignore_y=-100, average="macro").f1_score
compute_metrics = RegressionMetric(ignore_y=-100).mean_squared_error

for seed in seeds:
    seed_everything(seed)
    optimizer = torch.optim.AdamW(
        model.parameters(), lr=learning_rate, weight_decay=weight_decay
    )
    trainer = Trainer(
        model=model,
        train_loader=train_loader,
        eval_loader=valid_loader,
        test_loader=test_loader,
        batch_size=batch_size,
        epochs=epochs,
        optimizer=optimizer,
        compute_metrics=compute_metrics,
        device="cuda:0",
    )

    metrics = trainer.train()
    model.save("OmniGenome-52M", overwrite=True)
    print(metrics)

    model.load("OmniGenome-52M")
    output = model.inference(
        "GCCCGAAUAGCUCAGCCGGUUAGAGCACUUGACUGUUAAUCAGGGGGUCGUUGGUUCGAGUCCAACUUCGGGCGCCA"
    )
    print(output["predictions"])
