#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import re
import xml.etree.ElementTree as ET
from datetime import date
import spacy

"""Where data is inputted"""

__author__ = 'Daniel Campos, Sicong Huang, Hayley Luke, Simola Nayak, Shunjie Wang  '
__email__ = 'dacampos@uw.edu'

AQUAINT2_ROOT = 'Data/LDC02T31/'
DATA_ROOT = 'Data/'

# strings to remove from xml before parsing
CLEAN_RE = re.compile(r'\&.+;')

# examples:
# <doc id = "NYT19980903.0137" />
# /corpora/LDC/LDC02T31/nyt/1998/19980903_NYT
PATH_MAPPING = {
    'AQUAINT': {
        # Do some regex matching to build a path
        # (tag)(year)(group id).(doc id)
        'regex': re.compile(r'^([A-Z]{3})([0-9]{4})([0-9]{4})\.([0-9]{4})$'),
        'path': '{tag_lower}/{year}/{year}{group_id}_{tag}',
        'root': AQUAINT2_ROOT
    }
}


def build_path(doc_id):
    for corpus, info in PATH_MAPPING.items():
        match = info['regex'].match(doc_id)
        if not match:
            continue
        tag, year, group_id, doc_id = match.groups()
        original_tag = tag
        if tag == 'XIE':
            # No clue why the directory name is different than the file name
            tag = 'XIN'
        if tag != 'NYT':
            # Only the NYT doesn't have this suffix
            tag += '_ENG'
        path = info['path'].format(tag=tag, tag_lower=original_tag.lower(), year=year, group_id=group_id, doc_id=doc_id)
        return os.path.join(info['root'], path)
    # If we get here without returning, we didn't figure out the path
    print('Unable to find path for {doc_id}'.format(doc_id=doc_id))
    return None

class Sentence:
    def __init__(self, text, doc_headline, doc_date):
        self.text = text
        self.doc_headline = doc_headline
        self.doc_date = doc_date
    def set_text_parse(self, parse):
        self.text_nlp = parse
    def set_headline_parse(self, headline):
        self.headline_nlp = headline

class Document:
    def __init__(self, id, body, doc_date):
        self.id = id
        self.body = body
        self.doc_date = doc_date
        self.headline, self.text = self.clean_body(body)
        self.sentences = self.get_sentences(self.headline, self.text, self.doc_date)
    def get_sentences(self, headline, text, doc_date):
        sentences = []
        for sentence in text.split('.'):
            sentences.append(Sentence(sentence.replace('\n',''), headline, doc_date))
        return sentences
    def clean_body(self, body):
        '''
        Clean all tags out of the body element, leaving just the text, headline, date
        '''
        headline = body.findall('HEADLINE') or ''
        if headline != '':
            headline = headline[0].text.strip()
        text_el = body.find('TEXT')
        text = text_el.text.strip()
        if text == '':
            # Go through P tags
            for p in text_el.findall('P'):
                text += p.text.strip() + '\n'
        if text == '':
            # still didn't find any text? log it
            print('No text found for documents {id}'.format(id=self.id))
        return headline, text

class Topic:
    def __init__(self, id, title):
        self.id = id
        self.title = title
        # List of Document classes
        self.documents = []
    def load_doc(self, doc_id):
        path = build_path(doc_id)
        if not path:
            return
        with open(path, 'r') as f:
            contents = f.read()
        # Do some basic escaping, and add a root node
        # This is all very hacky, but the xml is extremely poorly formatted...
        # Get rid of amperstands entirely (maybe change in the future?)
        contents = CLEAN_RE.sub('', contents)
        contents = '<root>' + contents + '</root>'
        try:
            group_tree = ET.fromstring(contents)
        except ET.ParseError as e:
            print('Error parsing {path}'.format(path=path))
            print(e)
            raise e
        for child in group_tree.findall('DOC'):
            found_doc_id = child.find('DOCNO').text.strip()
            if doc_id == found_doc_id:
                # Add this document
                doc_date = child.find('DATE_TIME').text.strip()
                self.documents.append(Document(doc_id, child.find('BODY'), doc_date))

def get_topics(path_to_topic, args):
    '''
    Given a path to a topics xml, returns a list of Topic objects
    '''
    topic_tree = ET.parse(os.path.join(DATA_ROOT, path_to_topic))
    root = topic_tree.getroot()
    topics = []
    for child in root.findall('topic'):
        topic_id = child.attrib['id']
        title = child.find('title').text.strip()
        docset_a = child.find('docsetA')
        topic = Topic(topic_id, title)
        for doc in docset_a:
            doc_id = doc.attrib['id']
            topic.load_doc(doc_id)
        topics.append(topic)
    return topics

"""
if __name__ == '__main__':
    import ipdb; ipdb.set_trace()
    topics = get_topics('Documents/devtest/GuidedSumm10_test_topics.xml')
"""