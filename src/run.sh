#!/usr/bin/env bash
output_dir=$1
train_dir=$2
eval_dir=$3
model_dir=$4
exp_id=$5
rouge_dir=$8 # "/mnt/dropbox/19-20/573/code/ROUGE/"
rouge_config_file="../results/rouge_config_${exp_id}.xml"
rouge_output_file="../results/rouge_results_${exp_id}.txt"
python3 main.py 

# generate ROUGE config file
python3 "${rouge_dir}/create_config.py" ${output_dir} ${model_dir} ${rouge_config_file}

# generate ROUGE results
python3 "${rouge_dir}/run_rouge.py" ${rouge_config_file} > ${rouge_output_file}