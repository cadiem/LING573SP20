#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import re
import xml.etree.ElementTree as ET

"""Where data is inputted"""

__author__ = 'Daniel Campos, Sicong Huang, Hayley Luke, Simola Nayak, Shunjie Wang  '
__email__ = 'dacampos@uw.edu'

AQUAINT2_ROOT = './patas/AQUAINT-2'
DATA_ROOT = './patas/573/Data'

# examples:
# <doc id = "NYT19980903.0137" />
# /corpora/LDC/LDC02T31/nyt/1998/19980903_NYT
PATH_MAPPING = {
    'AQUAINT': {
        # Do some regex matching to build a path
        # (tag)(year)(group id).(doc id)
        'regex': re.compile(r'^([A-Z]{3})([0-9]{4})([0-9]{4})\.([0-9]{4})$'),
        'path': '{tag_lower}/{year}/{year}{group_id}_{tag}_ENG',
        'root': './patas/AQUAINT'
    }
}


def build_path(doc_id):
    for corpus, info in PATH_MAPPING.items():
        match = info['regex'].match(doc_id)

        if not match:
            continue

        tag, year, group_id, doc_id = match.groups()
        path = info['path'].format(tag=tag, tag_lower=tag.lower(), year=year, group_id=group_id, doc_id=doc_id)
        return os.path.join(info['root'], path)

    # If we get here without returning, we didn't figure out the path
    print('Unable to find path for {doc_id}'.format(doc_id))
    return None


class Topic:
    def __init__(self, id, title):
        self.id = id
        self.title = title

        # List of strings representing cleaned document text
        self.documents = []

    def load_doc(self, doc_id):
        path = build_path(doc_id)
        with open(path, 'r') as f:
            contents = f.read()

        # Do some basic escaping, and add a root node
        # This is all very hacky, but the xml is extremely poorly formatted...
        # Get rid of amperstands entirely (maybe change in the future?)
        contents = contents.replace('&AMP;', '')
        contents = '<root>' + contents + '</root>'
        group_tree = ET.fromstring(contents)

        for child in group_tree.findall('DOC'):
            found_doc_id = child.find('DOCNO').text.strip()
            if doc_id == found_doc_id:
                import ipdb; ipdb.set_trace()


def get_topics(path_to_topic):
    '''
    Given a path to a topics xml, returns a list of Topic objects
    '''
    topic_tree = ET.parse(os.path.join(DATA_ROOT, path_to_topic))
    root = topic_tree.getroot()

    topics = []
    for child in root.findall('topic'):
        topic_id = child.attrib['id']
        title = child.find('title')
        docset_a = child.find('docsetA')

        topic = Topic(topic_id, title)

        for doc in docset_a:
            doc_id = doc.attrib['id']
            topic.load_doc(doc_id)

    return topics


if __name__ == '__main__':
    topics = get_topics('Documents/devtest/GuidedSumm10_test_topics.xml')
