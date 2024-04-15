# -*- coding: utf-8 -*-
# file: ssp_pipeline.py
# time: 20:09 13/04/2024
# author: YANG, HENG <hy345@exeter.ac.uk> (杨恒)
# github: https://github.com/yangheng95
# huggingface: https://huggingface.co/yangheng
# google scholar: https://scholar.google.com/citations?user=NPq5a_0AAAAJ&hl=en
# Copyright (C) 2019-2024. All Rights Reserved.


from omnigenome.utility.pipeline_hub.pipeline import Pipeline
from omnigenome.utility.pipeline_hub.pipeline_hub import PipelineHub


from omnigenome.utility.pipeline_hub.pipeline import Pipeline


class SSPPipeline(Pipeline):
    def __init__(self, *args, **kwargs):
        super(SSPPipeline, self).__init__(*args, **kwargs)

    def launch_gradio_interface(self):
        import gradio as gr

        def predict(text):
            return self(text)["predictions"]

        gr.Interface(
            fn=predict,
            inputs=gr.Textbox(lines=3, label="Input"),
            outputs=gr.Textbox(label="Output"),
        ).launch()


pipeline = PipelineHub.load("Pipeline-RNA-SSP-Strand2")

pipeline.save("Pipeline-RNA-SSP-Strand2", overwrite=True)
pipeline.load("Pipeline-RNA-SSP-Strand2")

output = pipeline(
    "GCCCGAAUAGCUCAGCCGGUUAGAGCACUUGACUGUUAAUCAGGGGGUCGUUGGUUCGAGUCCAACUUCGGGCGCCA"
)

pipeline.train()
pipeline.save("Pipeline-RNA-SSP-Strand2-trained", overwrite=True)

pipeline.launch_gradio_interface()
