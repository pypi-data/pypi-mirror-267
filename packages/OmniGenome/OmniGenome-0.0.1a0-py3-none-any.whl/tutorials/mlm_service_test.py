# -*- coding: utf-8 -*-
# file: mlm_service_test.py
# time: 13:55 10/04/2024
# author: YANG, HENG <hy345@exeter.ac.uk> (杨恒)
# github: https://github.com/yangheng95
# huggingface: https://huggingface.co/yangheng
# google scholar: https://scholar.google.com/citations?user=NPq5a_0AAAAJ&hl=en
# Copyright (C) 2019-2024. All Rights Reserved.
from flask import Flask, request, jsonify
from transformers import AutoConfig, AutoTokenizer, AutoModelForMaskedLM
from omnigenome.src.model.mlm.model import OmniGenomeEncoderModelForMLM


# 预先加载模型和分词器，避免每次请求都重新加载
model_name_or_path = "pretrained_models/mprna_base_new"
# model_name_or_path = "pretrained_models/mprna_small_new"
config = AutoConfig.from_pretrained(model_name_or_path, trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
base_model = AutoModelForMaskedLM.from_pretrained(
    model_name_or_path, trust_remote_code=True
)
mlm_model = OmniGenomeEncoderModelForMLM(
    config, base_model, tokenizer=tokenizer, trust_remote_code=True
)

seq = f"ATGCGT{tokenizer.mask_token}ACG"
pred_seq = mlm_model.inference(seq)

app = Flask(__name__)


@app.route("/predict", methods=["POST", "GET"])
def predict():
    # 从请求中获取序列
    try:
        data = request.json
        seq = data.get("seq", "") if "seq" in data else data.get("sequence", "")
        if not seq:
            return jsonify({"error": "Empty sequence provided."})
        pred_seq = mlm_model.inference(seq)["predictions"]
        return jsonify({"predicted_sequence": pred_seq})
    except Exception as e:
        return jsonify({"error": str(e)})


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


label2id = {"(": 0, ")": 1, ".": 2}

# model_name_or_path = "pretrained_models/mprna_small_new"
model_name_or_path = "pretrained_models/mprna_base_new"
# model_name_or_path = "InstaDeepAI/segment_nt"
SN_tokenizer = OmniSingleNucleotideTokenizer.from_pretrained(model_name_or_path)

config = AutoConfig.from_pretrained(
    model_name_or_path, num_labels=len(label2id), trust_remote_code=True
)

ssp_model = OmniGenomeEncoderModelForTokenClassification(
    config,
    model_name_or_path,
    tokenizer=SN_tokenizer,
    label2id=label2id,
    trust_remote_code=True,
)

# ssp_model.load('OmniGenome-185M')
ssp_model.load("OmniGenome-185M-Strand2")


@app.route("/ss_predict", methods=["POST", "GET"])
def ss_predict():
    # 从请求中获取序列
    try:
        data = request.json
        seq = data.get("seq", "") if "seq" in data else data.get("sequence", "")
        if not seq:
            return jsonify({"error": "Empty sequence provided."})
        pred_seq = ssp_model.inference(seq)["predictions"]
        return jsonify({"predicted_sequence": pred_seq})
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
