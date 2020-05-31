#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Content here is realized"""
__author__ = 'Daniel Campos, Sicong Huang, Hayley Luke, Simola Nayak, Shunjie Wang  '
__email__ = 'dacampos@uw.edu,  huangs33@uw.edu, shunjiew@uw.edu, simnayak@uw.edu, jhluke@uw.edu'

import sys
import os
import re
import spacy
from data_input import Sentence

nlp = spacy.load("en_core_web_lg")

def processed_sentences(sentence_collection):
    return [nlp(sentence.text) for sentence in sentence_collection]

def break_large_sentences(sentence_collection, parse_collection, maxlen=7):
    newcollection = []
    for i in range(len(sentence_collection)):
        senttext = sentence_collection[i].text
        senttoks = [tok for tok in parse_collection[i]]
        currparse = [tag.dep_ for tag in parse_collection[i]]
        #break coordinating conjunctions and semicolons:
        if len(senttext) > maxlen:
            if ';' in senttext:
                twohalves = senttext.split(';')
                if len(twohalves[1].split(" ") > 3):
                    twohalves[1] = twohalves[1].strip().capitalize()
                    #append two sentences to array
                    newcollection.append(Sentence(twohalves[0], sentence_collection[i].doc_headline, sentence_collection[i].doc_date))
                    newcollection.append(Sentence(twohalves[1], sentence_collection[i].doc_headline, sentence_collection[i].doc_date))
            elif currparse.count('ROOT') > 1:
                splitdex = currparse.index('cc')
                twohalves = []
                twohalves[0] = ' '.join(senttoks[0:splitdex])
                twohalves[1] = ' '.join(senttoks[splitdex + 1:len(senttoks)])
                newcollection.append(Sentence(twohalves[0], sentence_collection[i].doc_headline, sentence_collection[i].doc_date))
                newcollection.append(Sentence(twohalves[1], sentence_collection[i].doc_headline, sentence_collection[i].doc_date))
            else:
                newcollection.append(sentence_collection[i])
        else:
            newcollection.append(sentence_collection[i])
    return newcollection

#remove extra nodes of the sentence parse tree- gratuitous modifiers
#please note, this could cause problems for phrases like "forcibly removed"
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
        sentence_collection[i].text = sentout
        #add to sentence collection
        output.append(sentence_collection[i])
    return output

#a redundancy hopefully: most such work will be done in preprocessing
def pre_clean(sentence_collection):
    for sentence in sentence_collection:
        #removing stray chars and punc and datelines
        sentence.text = re.sub(r"\([A-Z]+\, [A-Z][a-z]*\)", "", sentence.text)
        sentence.text = re.sub(r"[A-Z]+[a-z]*, [A-Z][a-z]*","", sentence.text)    
        sentence.text = re.sub(r"[\@\^\*\(\)\{\}\[\]\<\>\/\-\_\+\=\"\`]", "", sentence.text)
        sentence.text = re.sub(r"[A-Za-z]+\ {2,}", "", sentence.text)
        #use regexes to remove the bylines, datelines, etc.
    return sentence_collection

def realize_content(topics, summaries, output_dir, run_id):
    for topic in topics:
        print(topic.id)
        filename = '{}-A.M.100.{}.{}'.format(topic.id_1, topic.id_2, run_id)
        os.mkdir(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, filename), 'w') as w:
            summaries[topic.id] = pre_clean(summaries[topic.id])
            processed_sents = processed_sentences(summaries[topic.id])
            summaries[topic.id] = break_large_sentences(summaries[topic.id], processed_sents)
            processed_sents = processed_sentences(summaries[topic.id])
            summaries[topic.id] = remove_gratuitous_nodes(summaries[topic.id], processed_sents)
            for sentence in summaries[topic.id]:
                w.write("{}\n".format(sentence.text))