#!/bin/bash
source /home2/jhluke/LING573SP20/venv/bin/activate #please activate you ling573 environment accordingly
python src/main.py --corpus_config /dropbox/19-20/573/Data/Documents/devtest/GuidedSumm10_test_topics.xml --results_path results/D4_rouge_scores.out  --model_dir /dropbox/19-20/573/Data/models/devtest/ --output_dir outputs/D4/ --do_summarize 1
