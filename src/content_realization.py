#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Content here is realized"""
__author__ = 'Daniel Campos, Sicong Huang, Hayley Luke, Simola Nayak, Shunjie Wang  '
__email__ = 'dacampos@uw.edu,  huangs33@uw.edu, shunjiew@uw.edu, simnayak@uw.edu, jhluke@uw.edu'

import sys
import os
import re
import spacy
from datetime import datetime       #will help with removing stray dates

nlp = spacy.load("en_core_web_lg")

def processed_sentences(sentence_collection):
    return [nlp(sentence.text) for sentence in sentence_collection]

def sub_appropriate_corefs(sentence_collection):
    return sentence_collection

def break_large_sentences(sentence_collection):
    
    return sentence_collection

def combine_sentences(sentence_collection):
    #combine sentences for clarity, etc
    return sentence_collection

#remove extra branches of the sentence parse tree, from gratuitous modifiers
def remove_gratuitous_nodes(sentence_collection, parse_collection):
    output = []
    for i in range(len(sentence_collection)):
        sentout = ""
        sent = sentence_collection[i].text 
        parse = [tag.dep_ for tag in parse_collection[i]]
        
        for j in range(len(sent)):
            #exclude modifiers 
            if 'mod' in parse[j]:
                pass
            #no space after punct
            elif parse[j] == 'punct':
                sentout += sent[j]
            #space and then the word
            else:
                sentout += " "
                sentout += sent[j]
        words = sentout.split()
        
        #determiner agreement
        for i in range(len(words) - 1):
            if words[i] == 'a' and words[i + 1][0] in ['a','e','i','o','u']:
                words[i] = 'an'
            elif words[i] == 'an' and words[i + 1][0] not in ['a','e','i','o','u']:
                words[i] = 'a'
        sentout = " ".join(words)
        
        #add to sentence collection
        output.append(sentout)
    return output

#a redundancy hopefully: most such work will be done in preprocessing
def pre_clean(sentence_collection):
    #removing stray chars and punc
    re.sub("[@^*()\{\}\[\]<>/-_+=?!\"]", "", sentence_collection)
    #use regexes to remove the bylines, datelines, etc.
    re.sub("[A-Z]+, [A-Z][a-z]*","", sentence_collection)    
    return sentence_collection

def transformer_contreal(sentence_collection):
    return sentence_collection
    
def realize_content(topics, summaries, output_dir, run_id, use_transformer=False):
    for topic in topics:
        print(topic.id)
        filename = '{}-A.M.100.{}.{}'.format(topic.id_1, topic.id_2, run_id)
        with open(os.path.join(output_dir, filename), 'w') as w:
            summaries[topic.id] = pre_clean(summaries[topic.id])
            if not use_transformer:
                processed_sentences = processed_sentences(summaries[topic.id])
                summaries[topic.id] = combine_sentences(summaries[topic.id], processed_sentences)
                summaries[topic.id] = sub_appropriate_corefs(summaries[topic.id], processed_sentences)
                summaries[topic.id] = remove_gratuitous_nodes(summaries[topic.id], processed_sentences)
            else:
                summaries[topic.id] = transformer_contreal(summaries[topic.id])
            for sentence in summaries[topic.id]:
                w.write("{}\n".format(sentence.text))