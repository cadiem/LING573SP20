import os
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('config', help='path of the ROUGE config file')
    return parser.parse_args()

def main():
    args = parse_args()
    rouge_data = '/dropbox/19-20/573/code/ROUGE/data'
    perl_file = '/dropbox/19-20/573/code/ROUGE/ROUGE-1.5.5.pl'
    command = 'perl {} -e {} -a -n 2 -x -m -c 95 -r 1000 -f A -p 0.5 -t 0 -l 100 -s -d {}'.format(perl_file, rouge_data, args.config)
    os.system(command)

if __name__ == '__main__':
    main()
