#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Content here is realized"""
__author__ = 'Daniel Campos, Sicong Huang, Hayley Luke, Simola Nayak, Shunjie Wang  '
__email__ = 'dacampos@uw.edu'

import sys

#baseline implementation
#takes sentences in and writes them line-by-line to an output file
def realize_content(sentences):
    file = open("content_summary.txt", "w+")
    for sent in sentences:
        file.write(sent + "\n")
    file.close()