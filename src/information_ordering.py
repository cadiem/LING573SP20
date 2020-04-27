#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Information is ordered here"""

__author__ = 'Daniel Campos, Sicong Huang, Hayley Luke, Simola Nayak, Shunjie Wang  '
__email__ = 'dacampos@uw.edu,  huangs33@uw.edu, shunjiew@uw.edu, simnayak@uw.edu, jhluke@uw.edu'

def order_content(summaries):
    for topic_id in summaries:
        summaries[topic_id] = sorted(summaries[topic_id], key = lambda sentence: sentence.doc_date)
    return summaries