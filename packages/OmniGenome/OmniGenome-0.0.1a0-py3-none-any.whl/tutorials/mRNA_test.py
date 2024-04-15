# -*- coding: utf-8 -*-
# file: snp_test.py
# time: 14:22 06/04/2024
# author: YANG, HENG <hy345@exeter.ac.uk> (杨恒)
# github: https://github.com/yangheng95
# huggingface: https://huggingface.co/yangheng
# google scholar: https://scholar.google.com/citations?user=NPq5a_0AAAAJ&hl=en
# Copyright (C) 2019-2024. All Rights Reserved.

import torch
from sklearn.model_selection import train_test_split
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


class MRNADataset(OmniGenomeDatasetForTokenRegression):
    def __init__(self, data_source, tokenizer, max_length):
        super().__init__(data_source, tokenizer, max_length)

    def prepare_input(self, instance, **kwargs):
        target_cols = ["reactivity", "deg_Mg_pH10", "deg_Mg_50C"]
        instance["sequence"] = f'{instance["sequence"]}'
        tokenized_seq = self.tokenizer(
            instance["sequence"],
            padding="max_length",
            max_length=self.max_length,
            truncation=True,
            return_tensors="pt",
        )
        labels = [instance[target_col] for target_col in target_cols]
        # labels = np.concatenate(
        #     [
        #         np.array(labels),
        #         np.array(
        #             [
        #                 [-100] * (self.max_seq_len - len(labels[0])),
        #                 [-100] * (self.max_seq_len - len(labels[0])),
        #                 [-100] * (self.max_seq_len - len(labels[0])),
        #             ]
        #         ),
        #     ],
        #     axis=1,
        # ).T
        tokenized_seq["input_ids"] = tokenized_seq["input_ids"].squeeze()
        tokenized_seq["attention_mask"] = tokenized_seq["attention_mask"].squeeze()
        tokenized_seq["labels"] = (
            torch.tensor(labels, dtype=torch.float32).transpose(0, 1).squeeze()
        )
        return tokenized_seq


label2id = {"(": 0, ")": 1, ".": 2}

model_name_or_path = "pretrained_models/mprna_small_new"
# model_name_or_path = "pretrained_models/mprna_base_new"
SN_tokenizer = OmniSingleNucleotideTokenizer.from_pretrained(model_name_or_path)

config = AutoConfig.from_pretrained(
    model_name_or_path, num_labels=3, trust_remote_code=True
)

model = OmniGenomeEncoderModelForTokenRegression(
    config, model_name_or_path, tokenizer=SN_tokenizer, trust_remote_code=True
)

# epochs = 10
epochs = 1
learning_rate = 2e-5
weight_decay = 1e-5
batch_size = 8
seeds = [42]
# seeds = [45, 46, 47]

train_file = "benchmark/hgb_datasets/RNA-mRNA/train.json"
test_file = "benchmark/hgb_datasets/RNA-mRNA/test.json"

train_set = MRNADataset(
    data_source=train_file,
    tokenizer=SN_tokenizer,
    max_length=210,
)
test_set = MRNADataset(
    data_source=test_file,
    tokenizer=SN_tokenizer,
    max_length=210,
)
train_set, valid_set = train_test_split(
    train_set, test_size=0.1, random_state=42, shuffle=True
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
