#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Content here is realized"""
__author__ = 'Daniel Campos, Sicong Huang, Hayley Luke, Simola Nayak, Shunjie Wang  '
__email__ = 'dacampos@uw.edu,  huangs33@uw.edu, shunjiew@uw.edu, simnayak@uw.edu, jhluke@uw.edu'

import sys
import os
import re

def shrink_corefs(sentence_collection):
    return sentence_collection

def combine_sentences(sentence_collection):
    #combine sentences for clarity, etc
    return sentence_collection

def remove_gratuitous_nodes(sentence_collection):
    #remove extra branches of the sentence parse tree
    for sentence in sentence_collection:
        pass
        #TODO Parse and hack 
    return sentence_collection

def pre_clean(sentence_collection):
    #use regexes to remove the bylines, datelines, etc.
    re.sub("[A-Z]*,","", sentence_collection)
    return sentence_collection
    
def realize_content(topics, summaries, output_dir, run_id):
    for topic in topics:
        print(topic.id)
        filename = '{}-A.M.100.{}.{}'.format(topic.id_1, topic.id_2, run_id)
        with open(os.path.join(output_dir, filename), 'w') as w:
            pre_clean(summaries[topic.id])
            shrink_corefs(summaries[topic.id])
            remove_gratuitous_nodes(summaries[topic.id])
            combine_sentences(summaries[topic.id])
            for sentence in summaries[topic.id]:
                w.write("{}\n".format(sentence.text))