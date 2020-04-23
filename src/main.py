#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""A multi-doc extractive summarization system that evolves over time."""

__author__ = 'Daniel Campos, Sicong Huang, Hayley Luke, Simola Nayak, Shunjie Wang  '
__email__ = 'dacampos@uw.edu'

from data_input import get_topics
from content_selection import select_content 
from evaluation import eval_summary
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
    p.add_argument('--do_train', default = True)
    p.add_argument('--do_eval', default = True)
    p.add_argument('--do_summarize', default = True)
    p.add_argument('--output_dir', default ='../outputs')
    p.add_argument('--results_path', default='../results/D2_rouge_scores.out')
    p.add_argument('--model_dir', default = '/dropbox/19-20/573/Data/models/devtest')
    p.add_argument('--eval_script', default = '/dropbox/19-20/573/code/ROUGE/ROUGE-1.5.5.pl')
    p.add_argument('--rouge_data_dir', default = 'ROUGE/data')
    p.add_argument('--rouge_config_file', default = 'ROUGE/config.xml')
    p.add_argument('--method', default='Default')
    p.add_argument('--dampening', type=float, default=0.85)
    p.add_argument('--threshold', type=float, default=0.2)
    p.add_argument('--epsilon', type=float, default=0.1)
    p.add_argument('--min_words', type=int, default=5)
    p.add_argument('--word_vectors', default='en_core_web_lg')
    args = p.parse_args()

    if args.do_train:
        #train the model 
        #add some ML stuff here in later phases
        print("No training yet")
    if args.do_summarize:
        print("Loading Data")
        topics = get_topics('Documents/devtest/GuidedSumm10_test_topics.xml', args)
        print("selecting content")
        selected_content = select_content(topics, args.word_vectors, args.method, args.dampening, args.threshold, args.epsilon, args.min_words)
        ordered_content = order_content(selected_content)
        for topic in topics:
            print("Topic ID:{}\nTopic Title:{}\n".format(topic.id, topic.title))
            output = ''
            for sentence in ordered_content[topic.id]:
                output += '{}\n'.format(sentence.text)
            print(output)
        ordered_content = order_content(selected_content)
        realize_content = realize_content(ordered_content)
    if args.do_eval:
        create_config_file(args.output_dir, args.model_dir, args.rouge_config_file)
        run_rouge.run(args.eval_script, args.rouge_data_dir, args.rouge_config_file, args.results_path)
        print("Evaluation done")
