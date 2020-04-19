#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import xml.etree.ElementTree as ET

"""Where data is inputted"""

__author__ = 'Daniel Campos, Sicong Huang, Hayley Luke, Simola Nayak, Shunjie Wang  '
__email__ = 'dacampos@uw.edu'

AQUAINT_ROOT = './patas/573/AQUAINT'
AQUAINT2_ROOT = './patas/573/AQUAINT-2'
DATA_ROOT = './patas/573/Data'


def build_path(topic_id, doc_id):
    pass


class Topic:
    def __init__(self, id, title):
        self.id = id
        self.title = title

        # List of strings representing cleaned document text
        self.documents = []

    def load_doc(self, doc_id):
        path = build_path(self.id, doc_id)
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
