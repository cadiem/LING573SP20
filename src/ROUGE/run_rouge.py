import os

def run(perl_file, rouge_data, config, result_path):
    perl_file = '/dropbox/19-20/573/code/ROUGE/ROUGE-1.5.5.pl'
    command = 'perl {} -e {} -a -n 2 -x -m -c 95 -r 1000 -f A -p 0.5 -t 0 -l 100 -s -d {} > {}'.format(perl_file, rouge_data, config, result_path)
    os.system(command)

