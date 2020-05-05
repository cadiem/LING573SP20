#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""A multi-doc extractive summarization system that evolves over time."""

__author__ = 'Daniel Campos, Sicong Huang, Hayley Luke, Simola Nayak, Shunjie Wang  '
__email__ = 'dacampos@uw.edu,  huangs33@uw.edu, shunjiew@uw.edu, simnayak@uw.edu, jhluke@uw.edu'

from data_input import get_topics
from content_selection import select_content
from ROUGE.create_config import create_config_file
from ROUGE import run_rouge
from information_ordering import order_content
from content_realization import realize_content

from sys import argv
import argparse
import os
import spacy

if __name__ == '__main__':
    # Grab arguments
    p = argparse.ArgumentParser()
    p.add_argument('--do_train', default = False)
    p.add_argument('--do_eval', default = True)
    p.add_argument('--do_summarize', default = False)
    p.add_argument('--output_dir', default ='outputs/D2/')
    p.add_argument('--corpus_dir', default = '/corpora/LDC/')
    p.add_argument('--model_dir', default = '/dropbox/19-20/573/Data/models/devtest/')
    p.add_argument('--corpus_config', default = '/dropbox/19-20/573/Data/Documents/devtest/GuidedSumm10_test_topics.xml')
    p.add_argument('--results_path', default='results/D2_rouge_scores.out')
    p.add_argument('--eval_script', default = 'src/ROUGE/ROUGE-1.5.5.pl')
    p.add_argument('--rouge_data_dir', default = 'src/ROUGE/data')
    p.add_argument('--rouge_config_file', default = 'src/ROUGE/config.xml')
    p.add_argument('--method', default='Default', help ='Options include:Noun,Default,NoStop')
    p.add_argument('--dampening', type=float, default=0.8)
    p.add_argument('--threshold', type=float, default=0.3)
    p.add_argument('--epsilon', type=float, default=0.3)
    p.add_argument('--min_words', type=int, default=4)
    p.add_argument('--word_vectors', default='en_core_web_lg')
    p.add_argument('--run_id', default='1')
    p.add_argument('--is_local', default = False)
    p.add_argument('--do_load_data', default=False)
    p.add_argument('--use_checkpoint', default=False)
    args = p.parse_args()
    if args.is_local:
        args.corpus_dir = 'Data/'
        args.model_dir = 'Data/models/devtest/'
        args.corpus_config = 'Documents/devtest/GuidedSumm10_test_topics.xml'
    if args.do_train:
        #train the model add some ML stuff here in later phases
        print("No training yet")
    if args.do_load_data:
        print("Loading Data")
        topics = get_topics(args.corpus_dir, args.corpus_config, args.use_checkpoint)
    if args.do_summarize:
        print("Loading Data")
        topics = get_topics(args.corpus_dir, args.corpus_config, args.use_checkpoint, args.save_checkpoint)
        print("Selecting content")
        selected_content = select_content(topics, args.word_vectors, args.method, args.dampening, args.threshold, args.epsilon, args.min_words)
        print("Ordering content")
        ordered_content = order_content(selected_content)
        print("Realizing content")
        realize_content = realize_content(topics, ordered_content, args.output_dir, args.run_id)
    if args.do_eval:
        print("Starting evaluation")
        create_config_file(args.output_dir, args.model_dir, args.rouge_config_file)
        run_rouge.run(args.eval_script, args.rouge_data_dir, args.rouge_config_file, args.results_path)
        print("Evaluation done")
