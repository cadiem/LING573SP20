#!/usr/bin/env bash
output_dir=$1
train_dir=$2
eval_dir=$3
model_dir=$4
exp_id=$5
rouge_dir=$8 # "/mnt/dropbox/19-20/573/code/ROUGE/"
rouge_config_file="../results/rouge_config_${exp_id}.xml"
rouge_output_file="../results/rouge_results_${exp_id}.txt"
python main.py --do_summarize

# generate ROUGE config file
python "${rouge_dir}/create_config.py" ${output_dir} ${model_dir} ${rouge_config_file}

python main.py --do_eval --rouge_config_file ${rouge_config_file}