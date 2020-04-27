# LING573SP20
UW CLMS LING 573 Spring 2020 Document Summarization


LING 573: Language Processing Systems & Applications aka https://www.compling.uw.edu/academic-experience/courses/descriptions/#573


## Setup
To run you need to ensure you have a virtual enviroment that has the needed libraries on patas. To do so either use the one mentioned in run.sh or make your own. To make your own, see below. 

```
python3.7 -m venv 573-venv
. 573-venv/bin/activate
pip install spacy
python -m spacy download en_core_web_lg
```
## Usage
Once you have a correctly configured virtual enviorment go ahead an execute run.sh or D2.cmd if using a condor specific system. 

### New configurations

If you want to use any new configurations please modify run.sh to match the new desired config file, evaluation folder, output folder, results folder. 
the original contents of run.sh are posterity.
```
python src/main.py --corpus_config /dropbox/19-20/573/Data/Documents/devtest/GuidedSumm10_test_topics.xml --results_path results/D2_rouge_scores.out  --model_dir /dropbox/19-20/573/Data/models/devtest/ --output_dir outputs/D2/ --do_summarize 1
```

## Notes
When running our evaluation on Devtest we find that very few of the files have gold examples. we are not sure if there is a minor issue but for D1008 and above instead of finding D1009-A.M.A.* we find D1009-A.M.100.B.* and for that reason our evaluation is only averaging results on 7 documents. 
