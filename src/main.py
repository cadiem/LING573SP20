#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""A multi-doc extractive summarization system that evolves over time."""

__author__ = 'Daniel Campos, Sicong Huang, Hayley Luke, Simola Nayak, Shunjie Wang  '
__email__ = 'dacampos@uw.edu'

from data_input import get_topics
from content_selection import select_content 
#from info_ordering import * 
#from content_realization import *
#from evaluation import *

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
    p.add_argument('--results_dir', default = '../results/')
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
        for topic in topics:
            print("Topic ID:{}\nTopic Title:{}\n".format(topic.id, topic.title))
            output = ''
            for sentence in selected_content[topic.id]:
                output += '{}\n'.format(sentence.text)
            print(output)
        #ordered_content = order_content(selected_content)
        #realize_content = realize_content(ordered_content)
    if args.do_eval:
        #create a rouge config eval file
        #eval_summary(data_dir, config_file, output_path)
        print("No Eval yet")