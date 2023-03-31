# Path of the counter file
count_file=/tmp/.zsh_session_count

# Creation of tmp dir for logs
if [ -d /tmp/log-collector ]; then
    else
        mkdir /tmp/log-collector
    fi  

# If the file does not exist then create a counter set to value 1
if [[ ! -e $count_file ]] && [ -f /tmp/script_running ]; then
  echo "1" > $count_file
fi

# Increment the counter at every new terminal session
if [[ -f /tmp/script_running ]]; then
  session_count=$(($(cat $count_file) + 1))
  echo $session_count > $count_file
fi

# Code to run the script 
if [[ -z "$SCRIPT_RUN" ]] && [ -f /tmp/script_running ]; then
export SCRIPT_RUN=1
script -f $tty >(while read; do date +"%T.%3N";echo -n "$REPLY";done >> /tmp/log-collector/session_$session_count.log)
fi

# Hook which executes before every command 
preexec() {
    if [ -f /tmp/script_running ]; then
        echo $1 >> /tmp/log-collector/command_list$session_count.txt
    fi
}
