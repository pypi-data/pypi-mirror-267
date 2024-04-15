# -*- coding: utf-8 -*-
# file: test.py
# time: 14:22 06/04/2024
# author: YANG, HENG <hy345@exeter.ac.uk> (杨恒)
# github: https://github.com/yangheng95
# huggingface: https://huggingface.co/yangheng
# google scholar: https://scholar.google.com/citations?user=NPq5a_0AAAAJ&hl=en
# Copyright (C) 2019-2024. All Rights Reserved.
import autocuda
import torch
from transformers import AutoModel, AutoConfig

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
from omnigenome.utility.pipeline_hub.pipeline import Pipeline

label2id = {"(": 0, ")": 1, ".": 2}

model_name_or_path = "pretrained_models/mprna_small_new"
# model_name_or_path = "pretrained_models/mprna_base_new"
# model_name_or_path = "pretrained_models/mprna_large_new"
# model_name_or_path = "InstaDeepAI/segment_nt"
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

# epochs = 2
epochs = 1
learning_rate = 2e-5
weight_decay = 1e-5
batch_size = 4
seeds = [42]
# seeds = [45, 46, 47]

train_file = "benchmark/hgb_datasets/RNA-SSP-Strand2/train.json"
test_file = "benchmark/hgb_datasets/RNA-SSP-Strand2/test.json"
valid_file = "benchmark/hgb_datasets/RNA-SSP-Strand2/valid.json"
# train_file = "rna_secondary_structure_prediction/dataset/RFAM/train.json"
# test_file = "rna_secondary_structure_prediction/dataset/RFAM/test.json"
# valid_file = "rna_secondary_structure_prediction/dataset/RFAM/valid.json"

train_set = OmniGenomeDatasetForTokenClassification(
    data_source=train_file, tokenizer=SN_tokenizer, label2id=label2id, max_length=512
)
test_set = OmniGenomeDatasetForTokenClassification(
    data_source=test_file, tokenizer=SN_tokenizer, label2id=label2id, max_length=512
)
valid_set = OmniGenomeDatasetForTokenClassification(
    data_source=valid_file, tokenizer=SN_tokenizer, label2id=label2id, max_length=512
)
train_loader = torch.utils.data.DataLoader(
    train_set, batch_size=batch_size, shuffle=True
)
valid_loader = torch.utils.data.DataLoader(valid_set, batch_size=batch_size)
test_loader = torch.utils.data.DataLoader(test_set, batch_size=batch_size)

compute_metrics = ClassificationMetric(ignore_y=-100, average="macro").f1_score

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
    seeds=seeds,
    device=autocuda.auto_cuda(),
)

# metrics = trainer.train()
# model.save("OmniGenome-52M", overwrite=True)
# model.load("OmniGenome-52M")
#
# print(metrics)
# metrics.summary()

model.load("OmniGenome-52M")
output = model.inference(
    "GCCCGAAUAGCUCAGCCGGUUAGAGCACUUGACUGUUAAUCAGGGGGUCGUUGGUUCGAGUCCAACUUCGGGCGCCA"
)
print(output["predictions"])


pipeline = Pipeline(
    name="RNA-SSP-Strand2",
    model_name_or_path="OmniGenome-52M",
    tokenizer=SN_tokenizer,
    dataset={"train": train_set, "valid": valid_set, "test": test_set},
)

output = pipeline(
    "GCCCGAAUAGCUCAGCCGGUUAGAGCACUUGACUGUUAAUCAGGGGGUCGUUGGUUCGAGUCCAACUUCGGGCGCCA"
)

pipeline.save("Pipeline-RNA-SSP-Strand2")
