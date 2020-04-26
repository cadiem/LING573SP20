#!/bin/bash
source /home2/dacampos/LING573SP20/573-venv/bin/activate
python src/main.py --corpus_config /dropbox/19-20/573/Data/Documents/devtest/GuidedSumm10_test_topics.xml --results_path results/D2_rouge_scores.out  --model_dir /dropbox/19-20/573/Data/models/devtest/ --output_dir outputs/D2/ --do_summarize 1 
