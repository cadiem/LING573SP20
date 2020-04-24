#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Create config file to run evaluation"""

__author__ = 'Daniel Campos, Sicong Huang, Hayley Luke, Simola Nayak, Shunjie Wang  '
__email__ = 'dacampos@uw.edu,  huangs33@uw.edu, shunjiew@uw.edu, simnayak@uw.edu, jhluke@uw.edu'
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

###### Template is of this format ######
# <EVAL ID="D1001-A.M.100.A">
# <PEER-ROOT>/dropbox/18-19/573/Data/mydata</PEER-ROOT>
# <MODEL-ROOT>/dropbox/18-19/573/Data/models/devtest/</MODEL-ROOT>
# <INPUT-FORMAT TYPE="SPL"/>
# <PEERS>
# <P ID="1">D1001-A.M.100.A.1</P>
# </PEERS>
# <MODELS>
# <M ID="A">D1001-A.M.100.A.A</M>
# <M ID="B">D1001-A.M.100.A.B</M>
# <M ID="F">D1001-A.M.100.A.F</M>
# <M ID="H">D1001-A.M.100.A.H</M>
# </MODELS>
# </EVAL>
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
    out_dir_list = sorted(os.listdir(out_dir))
    model_dir_dict = {}
    for model_sum_name in os.listdir(model_dir):
        id = model_sum_name
        if id in model_dir_dict:
            model_dir_dict[id].append(model_sum_name)
        else:
            model_dir_dict[id] = [model_sum_name]

    # build tree
    root = ET.Element('ROUGE_EVAL', {'version': '1.5.5'})
    for sys_sum_name in out_dir_list:
        eval_elem = copy.deepcopy(template)
        eval_id, p_id = sys_sum_name.rsplit('.', 1)
        print(eval_id)
        eval_elem.set('ID', eval_id)
        peers = eval_elem.find('PEERS')
        p = ET.Element('P', {'ID': p_id})
        p.text = sys_sum_name
        peers.append(p)
        models = eval_elem.find('MODELS')
        print(model_dir_dict)
        for model_sum_name in sorted(model_dir_dict[eval_id]):
            m_id = model_sum_name.rsplit('.', 1)[1]
            m = ET.Element('M', {'ID': m_id})
            m.text = model_sum_name
            models.append(m)
        root.append(eval_elem)
    return root

def create_config_file(out_dir, model_dir, config_file):
    root = create_xml_tree(out_dir, model_dir)
    xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml()
    with open(config_file, 'w') as f:
        f.write(xmlstr[23:])
        f.write('\n')

def main():
    args = parse_args()
    create_config_file(args.out_dir, args.model_dir, args.rouge_config_file)

if __name__ == '__main__':
    main()
