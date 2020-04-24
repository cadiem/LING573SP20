#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Content here is realized"""
__author__ = 'Daniel Campos, Sicong Huang, Hayley Luke, Simola Nayak, Shunjie Wang  '
__email__ = 'dacampos@uw.edu,  huangs33@uw.edu, shunjiew@uw.edu, simnayak@uw.edu, jhluke@uw.edu'

import sys
import os

#baseline implementation
#takes sentences in and writes them line-by-line to an output file

def realize_content(topics, summaries, output_dir, run_id):
    for topic in topics:
        filename = '{}-A.M.100.A.{}'.format(topic.id, run_id)
        with open(os.path.join(output_dir, filename), 'w') as w:
            for sentence in summaries[topic.id]:
                w.write("{}\n".format(sentence.text))