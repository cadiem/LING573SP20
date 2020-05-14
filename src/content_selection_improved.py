#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Where content is selected"""

__author__ = 'Daniel Campos, Sicong Huang, Hayley Luke, Simola Nayak, Shunjie Wang  '
__email__ = 'dacampos@uw.edu,  huangs33@uw.edu, shunjiew@uw.edu, simnayak@uw.edu, jhluke@uw.edu'

import data_input

import math
import spacy
import numpy as np
import math

def normalize(text_input, nlp, method='Default'): 
    parse = nlp(text_input) 
    if method == "Noun":
        parse = nlp(' '.join([str(t) for t in parse if t.pos_ in ['NOUN', 'PROPN']]))
    elif method == 'NoStop':
        parse = nlp(' '.join([str(t) for t in parse if not t.is_stop]))
    return parse

def process_sentences(nlp, topics, method):
    for topic in topics:
        headline = topic.title
        for document in topic.documents:
            sentences = document.sentences
            headline_nlp = normalize(headline, nlp, method)
            for sentence in sentences:
                sentence.set_text_parse(normalize(sentence.text, nlp,  method))
                sentence.set_headline_parse(headline_nlp)
    return topics

def sentence_title_similarity(sentence, idf_dict, method = 'Default'):
    """ 
    Given a sentence compute its similarity with the topic title. Default method is word vector based
    ARGS: sentence(Sentence Class), method(string)
    Returns: float similarity
    """
    if method == 'idf-weighting':
        a_vector = weighted_sentence_vector(sentence.text_nlp, idf_dict)
        b_vector = weighted_sentence_vector(sentence.headline_nlp, idf_dict)
        return cosine_similarity(a_vector, b_vector)
    else:
        return sentence.text_nlp.similarity(sentence.headline_nlp)

def sentence_similarity(a, b, idf_dict, method = 'Default'):
    """ 
    Given two sentences produces their cosine similarity. Default is vector similarity
    ARGS: a(Sentence Class), b(Sentence Class), method(string)
    Returns: float similarity
    """
    if method == 'idf-weighting':
        a_vector = weighted_sentence_vector(a.text_nlp, idf_dict)
        b_vector = weighted_sentence_vector(b.text_nlp, idf_dict)
        return cosine_similarity(a_vector, b_vector)
    else:
        return a.text_nlp.similarity(b.text_nlp)

def weighted_sentence_vector(sentence_parse, idf_dict):
    idf_scores = np.empty(len(sentence_parse))
    word_vectors = []
    for i, token in enumerate(sentence_parse):
        idf_scores[i] = idf_dict.get(token.text, 0)
        word_vectors.append(token.vector)
    if np.sum(idf_scores) == 0.0:
        return np.zeros(len(word_vectors[0]))
    word_vectors = np.vstack(word_vectors)
    return np.average(word_vectors, axis=0, weights=idf_scores) 

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def get_sentences(docs, min_words):
    """ 
    Given a set of documents we extract all sentences that pass a minimum word threshold
    ARGS: docs(list of Documents), min_words(int)
    Returns: sentences(list of Sentences)
    """
    sentences = []
    for doc in docs:
        for sentence in doc.sentences:
            if len(sentence.text.split(' ')) >= min_words:
                sentences.append(sentence)
    return sentences

def build_topic_bias(sentences, idf_dict, method):
    """ 
    Given a list of sentence produce a vector representing the similarity between a topic title(question) and candidate sentences. 
    ARGS: sentences(list), method(string)
    Returns: list of distance of each sentence to title(query)
    """
    similarity = []
    for sentence in sentences:
        similarity.append(sentence_title_similarity(sentence, idf_dict, method))
    similarity_sum = np.sum(similarity)
    if similarity_sum == 0:
        similarity_sum = 1
    return np.array(similarity)/ similarity_sum #normalize


def build_matrix(similarity_matrix, topic_bias, dampening):
    """ 
    Given a sentence similarity matrix, a topic bias vector and a dampening factor produce a unified matrix representation. 
    ARGS: similarity_matrix(2d matrix), topic_bias(1d vector), dampening(float)
    Returns: unified matrix(1d)
    """
    return (dampening * (topic_bias)) + ((1-dampening) * (similarity_matrix))

def build_similarity_matrix(sentences, threshold, idf_dict, method):
    """ 
    Given sentences we Builds and returns a 2D numpy matrix of inter-sentential cosine similarity.
    ARGS: sentences(list), threshold(float), method(str) defining cosine similarity method
    Returns: 2d matrix
    """
    sentence_count = len(sentences)
    similarities = np.zeros((sentence_count, sentence_count))
    for i in range(sentence_count):
        for j in range(i, sentence_count):
            tmp = 1 #default similarity
            if i != j:
                tmp = sentence_similarity(sentences[i], sentences[j], idf_dict, method)
                if tmp > threshold:
                    similarities[i][j] = tmp
                    similarities[j][i] = tmp
    sums = similarities.sum(axis = 1, keepdims=True)
    return similarities/sums #normalize

def get_lex_rank(sentences, matrix, epsilon):
    """ 
    a matrix and an epsilon value representing the lexical rank of sentences for summaries we use the power method to find lexrank values. 
    ARGS: matrix(2d) representing lexrank method
    Returns:  probabilities(1d vector)
    """
    sentence_count = len(sentences)
    probabilities = np.ones(sentence_count)/sentence_count # set even sampling probs
    diff = 1
    while diff > epsilon:
        tmp = np.dot(matrix, probabilities)
        diff = np.linalg.norm(np.subtract(tmp,probabilities))
        probabilities = tmp
    return probabilities

def is_not_too_similar(candidate_sentence, already_selected_sentences, idf_dict, method):
    """ 
    Given a candidate sentence compare to all other already selected sentence and keep only those that aren't within 0.6 of another sentence
    ARGS: candidate_sentence(Sentence), already_selected_sentences(list), method(str)
    Returns: Bool
    """
    similarities = []
    for sentence in already_selected_sentences:
        #print("Sentence 1:{}\nSentence2:{}\nSimilarity:{}".format(candidate_sentence.text, sentence.text,sentence_similarity(candidate_sentence, sentence, method)))
        if sentence_similarity(candidate_sentence, sentence, idf_dict, method) >= 0.7:
            return False
    return True

def get_lex_rank_sorted_sentences(lex_rank_scores):
    """ 
    Given a list of lex rank scores produce an list representing sentence order sorted by lexrank value
    ARGS: lex_rank_scores(list)
    Returns: lex_rank_sorted_keys(list)
    """
    lex_rank_index_to_score = {}
    for i in range(len(lex_rank_scores)):
        lex_rank_index_to_score[i] = lex_rank_scores[i]
    return list({k: v for k, v in sorted(lex_rank_index_to_score.items(), key=lambda item: item[1], reverse=True)}.keys())

def select_sentences(sentences, sentence_ids_sorted_by_lex_rank, idf_dict, method):
    """ 
    Given a set of sentences and a sorted index via lex rank produce candidate summary by greedily looping over candidates and removing any that make summary > 100 words or are similar to other already selected sentences
    Takes a list of sentences sorted by LexRank value (descending) and selects the sentences to add to the summary greedily based on LexRank value
    while excluding sentences with cosine similarity > 0.6to any sentence already in the summary.
    ARGS: sentences(List of Sentence obj), sentence_ids_sorted_by_lex_rank(list) an ordered list of indexes for sentences based on lexrank score, method(str) setting the cosine comparison method
    Returns: candidate sentences for summary
    """
    current_summary_size = 0
    selected_sentences = []
    for i in sentence_ids_sorted_by_lex_rank:
        cur_sentence_len = len(sentences[i].text.split())
        if cur_sentence_len + current_summary_size < 100:
            if is_not_too_similar(sentences[i], selected_sentences, idf_dict, method):
                current_summary_size += cur_sentence_len
                selected_sentences.append(sentences[i])
    return selected_sentences

def build_idf_scores(topics, nlp):
    '''
    Given topics and spacy model, compute idf score of all tokens present in corpus
    ARGS: topics(List of Topic obj), nlp(spacy model)
    Returns: idf scores(dictionary)
    '''
    df = dict()
    doc_count = 0
    for topic in topics:
        for document in topic.documents:
            doc_count += 1
            for sentence in document.sentences:
                for token in sentence.text_nlp:
                    if df.get(token.text, 0) < doc_count:
                        df[token.text] = df.get(token.text, 0) + 1
    idf = {token: math.log(doc_count / count) for token, count in df.items()}
    return idf

def select_content(topics, word_vectors, method, dampening, threshold, epsilon, min_words):
    """
    Given a bunch of topics method iterates and creates summaries of <= 100 words using full sentences 
    Method uses Biased LExRank Similarity Graph algorithm.
    ARGS: topics, a dampening factor, a inter sentence threshold, an epsilon, min_words
    Returns:
    """
    print("loading spacy")
    nlp = spacy.load(word_vectors)
    process_sentences(nlp, topics, method)
    idf_dict = build_idf_scores(topics, nlp)
    summaries = {}
    for topic in topics:
        #Get Sentences, process sentences, build similarity matrix, sentence title bias, build markov Matrix, Calculate lexrank, sort sentences by score
        sentences = get_sentences(topic.documents, min_words)
        similarity_matrix = build_similarity_matrix(sentences, threshold, idf_dict, method)
        topic_bias = build_topic_bias(sentences, idf_dict, method)
        matrix = build_matrix(similarity_matrix, topic_bias, dampening)
        lex_rank_scores = get_lex_rank(sentences, matrix.T, epsilon) # we trampose matrix for easy math
        sentence_ids_sorted_by_lex_rank = get_lex_rank_sorted_sentences(lex_rank_scores)   
        summaries[topic.id] = select_sentences(sentences , sentence_ids_sorted_by_lex_rank, idf_dict, method)
    return summaries    
