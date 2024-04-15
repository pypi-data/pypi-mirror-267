# -*- coding: utf-8 -*-
# file: test.py
# time: 14:22 06/04/2024
# author: YANG, HENG <hy345@exeter.ac.uk> (杨恒)
# github: https://github.com/yangheng95
# huggingface: https://huggingface.co/yangheng
# google scholar: https://scholar.google.com/citations?user=NPq5a_0AAAAJ&hl=en
# Copyright (C) 2019-2024. All Rights Reserved.
import json

import numpy as np
import torch
from transformers import AutoConfig

from omnigenome.src.dataset.omnigenome_dataset import (
    OmniGenomeDatasetForTokenClassification,
)
from omnigenome.src.metric.classification_metric import ClassificationMetric
from omnigenome.src.misc.utils import seed_everything
from omnigenome.src.tokenizer.single_nucleotide_tokenizer import (
    OmniSingleNucleotideTokenizer,
)
from omnigenome.src.model.classiifcation.model import (
    OmniGenomeEncoderModelForTokenClassification,
)
from omnigenome.src.trainer.trainer import Trainer

label2id = {"Normal": 0, "Mutation": 1}

model_name_or_path = "pretrained_models/mprna_small_new"
# model_name_or_path = "pretrained_models/mprna_base_new"
SN_tokenizer = OmniSingleNucleotideTokenizer.from_pretrained(model_name_or_path)

config = AutoConfig.from_pretrained(
    model_name_or_path, num_labels=len(label2id), trust_remote_code=True
)

model = OmniGenomeEncoderModelForTokenClassification(
    config,
    model_name_or_path,
    tokenizer=SN_tokenizer,
    label2id=label2id,
    trust_remote_code=True,
)

# epochs = 20
epochs = 1
learning_rate = 2e-5
weight_decay = 1e-5
batch_size = 8
seeds = [42]
# seeds = [45, 46, 47]

train_file = "benchmark/hgb_datasets/RNA-SNMR/train.json"
test_file = "benchmark/hgb_datasets/RNA-SNMR/test.json"
valid_file = "benchmark/hgb_datasets/RNA-SNMR/valid.json"


class SNMRDataset(OmniGenomeDatasetForTokenClassification):
    def prepare_input(self, instance, **kwargs):
        sequence = instance.get("seq", None)
        mutation = instance.get("mut", None)
        labels = [1 if mutation[i] != sequence[i] else 0 for i in range(len(sequence))]

        tokenized_inputs = self.tokenizer(
            " ".join(list(mutation)),
            padding="do_not_pad",
            truncation=True,
            max_length=self.max_length,
            return_tensors="pt",
            **kwargs
        )
        tokenized_inputs["input_ids"] = tokenized_inputs["input_ids"].squeeze()
        tokenized_inputs["attention_mask"] = tokenized_inputs[
            "attention_mask"
        ].squeeze()
        if labels is not None:
            labels = np.array(labels, dtype=np.int64)
            labels = labels.reshape(-1)
            padded_labels = np.concatenate([[-100], labels, [-100]])
            tokenized_inputs["label"] = torch.tensor(padded_labels, dtype=torch.int64)
        return tokenized_inputs


train_set = SNMRDataset(
    data_source=train_file, tokenizer=SN_tokenizer, label2id=label2id, max_length=210
)
test_set = SNMRDataset(
    data_source=test_file, tokenizer=SN_tokenizer, label2id=label2id, max_length=210
)
valid_set = SNMRDataset(
    data_source=valid_file, tokenizer=SN_tokenizer, label2id=label2id, max_length=210
)
train_loader = torch.utils.data.DataLoader(
    train_set, batch_size=batch_size, shuffle=True
)
valid_loader = torch.utils.data.DataLoader(valid_set, batch_size=batch_size)
test_loader = torch.utils.data.DataLoader(test_set, batch_size=batch_size)

compute_metrics = ClassificationMetric(ignore_y=-100, average="macro").roc_auc_score

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
        # "GCCCGAAUAGCUCAGCCGGUUAGAGCACUUGACUGUUAAUCAGGGGGUCGUUGGUUCGAGUCCAACUUCGGGCGCCA"
        "AATAAGGCTTTATGAGTAAGCCAGTTTGCGAGGGTGGGGGTTATAATCGAGCAAGCTAGTATGGGGGGTAATAATAG"
    )
    print(output["predictions"])
