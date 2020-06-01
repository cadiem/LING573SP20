universe=vanilla
executable = /bin/bash
getenv = true
output = stdout_evaltest
error = stderr_evaltest
log = log_evaltest
notification = complete
arguments = "run_evaltest.sh"
transfer_executable = false 
request_memory = 2*1024
queue
