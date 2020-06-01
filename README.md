# LING573SP20
UW CLMS LING 573 Spring 2020 Document Summarization


LING 573: Language Processing Systems & Applications aka https://www.compling.uw.edu/academic-experience/courses/descriptions/#573


## Setup
To run you need to ensure you have a virtual environment that has the needed libraries on patas. To do so either use the one mentioned in run.sh or make your own. To make your own, see below. 

```
python3.6 -m venv 573-venv
. 573-venv/bin/activate
pip install spacy
pip install -U sentence-transformers
python -m spacy download en_core_web_lg
```
## Usage
Once you have a correctly configured virtual environment go ahead an execute run.sh or D4.cmd if using a condor specific system. 

### New configurations

If you want to use any new configurations please modify run.sh to match the new desired config file, evaluation folder, output folder, results folder. 
the original contents of run.sh are posterity.
```
python src/main.py --corpus_config /dropbox/19-20/573/Data/Documents/devtest/GuidedSumm10_test_topics.xml --results_path results/D4_rouge_scores.out  --model_dir /dropbox/19-20/573/Data/models/devtest/ --output_dir outputs/D4/ --do_summarize 1
```
