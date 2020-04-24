#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""We evaluate"""

__author__ = 'Daniel Campos, Sicong Huang, Hayley Luke, Simola Nayak, Shunjie Wang  '
__email__ = 'dacampos@uw.edu'

import subprocess
from subprocess import Popen, PIPE

def eval_summary(data_dir, config_file, output_path):
	results=open(output_path, 'w+')
	results.write(subprocess.check_output('ROUGE/ROUGE-1.5.5.pl -e {} -a -n 2 -x -m -c 95 -r 1000 -f A -p 0.5 -t 0 -l 100 -s -d {}'.format(data_dir, config_file).split()).decode())
	results.close()