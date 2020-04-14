#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""A multi-doc extractive summarization system that evolves over time."""

__author__ = 'Daniel Campos, Sicong Huang, Hayley Luke, Simola Nayak, Shunjie Wang  '
__email__ = 'dacampos@uw.edu'

from data_input import * 
from content_selection import * 
from info_ordering import * 
from content_realization import *
from evaluation import *

from sys import argv
import argparse
import os

if __name__ == '__main__':
    # Grab arguments
    p = argparse.ArgumentParser()
    p.add_argument('--do_train', default = True)
    p.add_argument('--do_eval', default = True)
    p.add_argument('--output_dir', default ='../outputs')
    p.add_argument('--results_dir', default = '../results/')
    p.add_argument('--eval_file')
    p.add_argument('--steming', default = False)
    p.add_argument('--lower', default = False)
    args = p.parse_args()
    if do_train:
        #train the model
    if do_eval:
        #load data from p.eval_file
        #select content
        #order content
        #realize content 
        #prep and evaluate content
