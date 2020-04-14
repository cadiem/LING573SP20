#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""A multi-doc extractive summarization system that evolves over time."""

__author__ = 'Daniel Campos, Sicong Huang, Hayley Luke, Simola Nayak, Shunjie Wang  '
__email__ = 'dacampos@uw.edu'

from data_input import get_data
from content_selection import select_content
from info_ordering import order_content
from content_realization import *
from evaluation import eval_summaries

from sys import argv
import argparse
import os

def write_summaries(ordered_summaries, output_dir, exp_id=1):
    """
    Take a list of topics each with summaries and outputs the summaries in a format we can evaluate. 
    Args:

    Returns:
        None
    """
    for topic in ordered_summaries:
        current_topic_id = topic['topic_id']
        id_0 = current_topic_id[:-1]
        id_1 = current_topic_id[-1:]
        filename = os.path.join(output_dir + '{}-A.M.100.{}.{}'.format(id_0,id_1, exp_id) )
        dir_path = os.path.dirname(filename)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        with open(filepath,'w') as w:
            for sentence in topic.summary:
                w.write('{}\n'.format(sentence))

if __name__ == '__main__':
    # Grab arguments
    p = argparse.ArgumentParser()
    p.add_argument('--do_train', default = False)
    p.add_argument('--do_eval', default = True)
    p.add_argument('--output_dir', default ='../outputs')
    p.add_argument('--results_dir', default = '../results/')
    p.add_argument('--eval_file')
    p.add_argument('--exp_id', default='42')
    p.add_argument('--steming', default = False)
    p.add_argument('--lower', default = False)
    args = p.parse_args()
    if args.do_train:
        #train the model some ML goes here eventually
    if args.do_eval:
        topics = get_data()
        sentences = select_content(topics)
        ordered_summaries = order_content(sentences)
        write_summaries(ordered_summaries, args.output_dir, exp_id)
        eval_summaries(args.output_dir, test_type)
        #load data from p.eval_file
        #select content
        #order content
        #realize content 
        #prep and evaluate content
