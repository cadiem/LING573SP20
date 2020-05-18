#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Information is ordered here"""

__author__ = 'Daniel Campos, Sicong Huang, Hayley Luke, Simola Nayak, Shunjie Wang  '
__email__ = 'dacampos@uw.edu,  huangs33@uw.edu, shunjiew@uw.edu, simnayak@uw.edu, jhluke@uw.edu'

import spacy
import numpy as np
from itertools import permutations
from random import sample
import os
import random
import subprocess

TRAIN_DIR = "/dropbox/19-20/573/Data/models/training/2009"
MODEL_DIR = "svm/"
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)
SVM_RANK_DIR = "/NLP_TOOLS/ml_tools/svm/svm_rank/latest/"

nlp = spacy.load("en_core_web_lg")
sentencizer = nlp.create_pipe("sentencizer")
nlp.add_pipe(sentencizer)

def create_grid(document: list) -> dict:
    grid = dict()
    for i, sentence in enumerate(document):
        for token in nlp(sentence):
            if token.pos_ in ["NOUN", "PROPN"]:
                if token.dep_ in ["iobj", "pobj", "obj"]:
                    label = 'O'
                elif token.dep_ in ["csubj", "nsubj", "csubjpass", "nsubjpass"]:
                    label = 'S'
                else:
                    label = 'X'
                if token.text in grid:
                    grid[token.text][i] = label
                else:
                    grid[token.text] = {i: label}
    return grid

def grid_to_vec(grid: dict) -> np.ndarray:
    transition_freq = dict()
    for label1 in ["S","O","X","-"]:
        for label2 in ["S","O","X","-"]:
            transition_freq[label1+label2] = 0
    for entity in grid:
        for i in range(len(grid.keys()) - 1):
            transition = grid[entity].get(i, '-') + grid[entity].get(i+1, '-')
            transition_freq[transition] += 1

    transition_sum = sum(transition_freq.values())
    for freq in transition_freq:
        prob = transition_freq[freq]/transition_sum
        transition_freq[freq] = prob

    doc_vec = np.array(list(transition_freq.values()))
    return doc_vec

def print_grid(grid: dict):
    print("  ", end='')
    for entity in grid:
        print(entity[0], end=' ')
    print('\n',end='')
    for i in range(len(grid.keys())):
        print(i, end=' ')
        for entity in grid:
            print(grid[entity].get(i, '-'), ' ', sep='',end='')
        print('\n', end='')

def create_train_file(model_dir, output_file):
    with open(os.path.join(model_dir, output_file), "w+") as out:
        sampled_docs = random.sample(os.listdir(TRAIN_DIR), 80)
        qid = 1
        for doc in sampled_docs:
            with open(os.path.join(TRAIN_DIR, doc)) as doc_file:
                document = doc_file.readline()
                document = nlp(document.strip()) #Divide paragraph to sentences
                ordered_sents = [sent.text for sent in document.sents]
                all_perms = list(permutations(ordered_sents))
                if len(all_perms) < 20:
                    sampled_perms = all_perms
                else:
                    sampled_perms = sample(all_perms, 20)
                ordered_grid = create_grid(ordered_sents)
                ordered_vec = grid_to_vec(ordered_grid)
                for shuffled_sents in sampled_perms:
                    shuffled_grid = create_grid(shuffled_sents)
                    shuffled_vec = grid_to_vec(shuffled_grid)
                    print(2, ' qid:', qid, end=' ', sep='', file=out)
                    for feat_id, feat in enumerate(ordered_vec):
                        print(feat_id+1, ":", feat, sep = '', end=' ', file=out)
                    print("\n", end='', file=out)
                    print(1, ' qid:', qid, end=' ', sep='', file=out)
                    for feat_id, feat in enumerate(shuffled_vec):
                        print(feat_id+1, ":", feat, sep = '', end=' ', file=out)
                    print("\n", end='', file=out)
                    qid += 1

def train_svm(train_file, model_file):
    subprocess.Popen(SVM_RANK_DIR + "svm_rank_learn -c 20.0 " + MODEL_DIR + train_file + " " + MODEL_DIR + model_file, shell=True).wait()

def svm_predict(summaries, test_file, model_file, pred_file):
    for topic_id in summaries:
        candidates = list()
        with open(os.path.join(MODEL_DIR, test_file), "w+") as out:
            qid = 1
            # First sort each summ chronologically by sentence doc date
            summaries[topic_id] = sorted(summaries[topic_id], key = lambda sentence: sentence.doc_date)
            candidates.append(summaries[topic_id])
            ordered_sents = [sentence.text for sentence in summaries[topic_id]]
            all_perms = list(permutations(summaries[topic_id]))
            if len(all_perms) < 19:
                sampled_perms = all_perms
            else:
                sampled_perms = sample(all_perms, 19)
            candidates += sampled_perms
            ordered_grid = create_grid(ordered_sents)
            ordered_vec = grid_to_vec(ordered_grid)
            # Chronological ordered paragraph is the first candidate
            print(0, ' qid:', qid, end=' ', sep='', file=out)
            for feat_id, feat in enumerate(ordered_vec):
                print(feat_id+1, ":", feat, sep = '', end=' ', file=out)
            print("\n", end='', file=out)
            qid += 1
            for shuffled_sents in sampled_perms:
                shuffled_sents = [sent.text for sent in shuffled_sents]
                shuffled_grid = create_grid(shuffled_sents)
                shuffled_vec = grid_to_vec(shuffled_grid)
                print(0, ' qid:', qid, end=' ', sep='', file=out)
                for feat_id, feat in enumerate(shuffled_vec):
                    print(feat_id+1, ":", feat, sep = '', end=' ', file=out)
                print("\n", end='', file=out)
                qid += 1

        subprocess.Popen(SVM_RANK_DIR + "svm_rank_classify " + MODEL_DIR + test_file + " " + MODEL_DIR + model_file + " " + MODEL_DIR + pred_file, shell=True).wait()

        with open(os.path.join(MODEL_DIR, pred_file)) as pred:
            cand_id = 0
            cand_scores = list()
            for score in pred:
                cand_scores.append((cand_id, float(score)))
            cand_scores = sorted(cand_scores, key = lambda pair: pair[1], reverse=True)
            winner_id = cand_scores[0][0]
        
        summaries[topic_id] = candidates[winner_id]
    
    return summaries

def order_content_chrono(summaries):
    for topic_id in summaries:
        summaries[topic_id] = sorted(summaries[topic_id], key = lambda sentence: sentence.doc_date)
    return summaries

def order_content(summaries):
    if not os.path.exists(os.path.join(MODEL_DIR, "train.dat")):
        create_train_file(MODEL_DIR, "train.dat")
    if not os.path.exists(os.path.join(MODEL_DIR, "model")):
        train_svm("train.dat","model")
    return svm_predict(summaries, "test.dat", "model", "pred")