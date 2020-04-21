#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import argparse
import xml.etree.ElementTree as ET
from xml.dom import minidom
import copy

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('out_dir', help='system output directory')
    parser.add_argument('model_dir', help='human summaries directory')
    parser.add_argument('rouge_config_file', help='ROUGE configuration file')
    return parser.parse_args()

def create_elem_template(out_dir, model_dir):
    template = ET.Element('EVAL')
    peer_root = ET.Element('PEER-ROOT')
    peer_root.text = out_dir
    model_root = ET.Element('MODEL-ROOT')
    model_root.text = model_dir
    input_format = ET.Element('INPUT-FORMAT', {'TYPE': 'SPL'})
    peers = ET.Element('PEERS')
    models = ET.Element('MODELS')
    template.append(peer_root)
    template.append(model_root)
    template.append(input_format)
    template.append(peers)
    template.append(models)
    return template

def create_xml_tree(out_dir, model_dir):
    template = create_elem_template(out_dir, model_dir)
    out_dir_list = os.listdir(out_dir)
    model_dir_dict = {}
    for model_sum_name in os.listdir(model_dir):
        id = model_sum_name.rsplit('.', 1)[0]
        if id in model_dir_dict:
            model_dir_dict[id].append(model_sum_name)
        else:
            model_dir_dict[id] = [model_sum_name]

    # build tree
    root = ET.Element('ROUGE_EVAL', {'version': '1.5.5'})
    for sys_sum_name in out_dir_list:
        eval_elem = copy.deepcopy(template)
        eval_id = sys_sum_name.rsplit('.', 1)[0]
        eval_elem.set('ID', eval_id)
        peers = eval_elem.find('PEERS')
        peers.text = sys_sum_name
        models = eval_elem.find('MODELS')
        for model_sum_name in model_dir_dict[eval_id]:
            m_id = model_sum_name.rsplit('.', 1)[1]
            m = ET.Element('M', {'ID': m_id})
            m.text = model_sum_name
            models.append(m)
        root.append(eval_elem)
    return root

def main():
    args = parse_args()
    template = create_elem_template(args.out_dir, args.model_dir)
   
    tree = ET.ElementTree(template)
    # tree.write('o.xml', short_empty_elements=False)
    xmlstr = minidom.parseString(ET.tostring(template)).toprettyxml()
    # print(xmlstr)
    with open('o.xml', 'w') as f:
        f.write(xmlstr)

if __name__ == '__main__':
    main()
