#!/bin/bash
git clone https://github.com/SKTBrain/KoBERT.git
pip install --default-timeout=100 -r KoBERT/requirements.txt
pip install KoBERT/.
git clone https://github.com/BM-K/KoSentenceBERT_SKTBERT.git
pip install -r KoSentenceBERT_SKTBERT/requirements.txt
pip install newspaper3k
rm -rf /opt/conda/lib/python3.7/site-packages/transformers
rm -rf /opt/conda/lib/python3.7/site-packages/tokenizers
rm -rf /opt/conda/lib/python3.7/site-packages/sentence_transformers
cp -r KoSentenceBERT_SKTBERT/transformers /opt/conda/lib/python3.7/site-packages/transformers
cp -r KoSentenceBERT_SKTBERT/tokenizers /opt/conda/lib/python3.7/site-packages/tokenizers
cp -r KoSentenceBERT_SKTBERT/sentence_transformers /opt/conda/lib/python3.7/site-packages/sentence_transformers
mkdir KoSentenceBERT_SKTBERT/output/training_sts/0_Transformer
cp sts/result.pt KoSentenceBERT_SKTBERT/output/training_sts/0_Transformer/result.pt
rm -rf /opt/conda/lib/python3.7/site-packages/torch/serialization.py
cp serialization.py /opt/conda/lib/python3.7/site-packages/torch/serialization.py

