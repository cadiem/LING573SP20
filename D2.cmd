universe=vanilla
executable = run.sh
getenv = true
output = stdout
error = stderr
log = log
notification = complete
arguments = "--do_eval True --results_path results/D2=_rouge_scores.out --output_dir outputs/D2/"
transfer_executable = false 
request_memory = 2*1024
queue
