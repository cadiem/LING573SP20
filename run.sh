#!/bin/bash
source /home2/dacampos/LING573SP20/573-venv/bin/activate #please activate you ling573 environment accordingly
python src/main.py --corpus_config /dropbox/19-20/573/Data/Documents/devtest/GuidedSumm10_test_topics.xml --results_path results/D3_rouge_scores.out  --model_dir /dropbox/19-20/573/Data/models/devtest/ --output_dir outputs/D3/ --do_summarize 1