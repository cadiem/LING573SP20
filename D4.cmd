universe=vanilla
executable = /bin/bash
getenv = true
output = stdout_devtest
error = stderr_devtest
log = log_devtest
notification = complete
arguments = "run.sh"
transfer_executable = false 
request_memory = 2*1024
arguments = "./run.sh"
transfer_executable=false
queue
