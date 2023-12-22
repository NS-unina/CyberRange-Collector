# Path of the counter file
# count_file=/tmp/.zsh_session_count
export CYBER_RANGE_COLLECTOR_PATH=~/.cyber-range-collector

function get_date {
  date +"%T.%3N"
}

# Creation of tmp dir for logs
if [ -d /tmp/log-collector ]; then
    else
        mkdir /tmp/log-collector
    fi  

# If the file does not exist then create a counter set to value 1
# if [[ ! -e $count_file ]] && [ -f /tmp/script_running ]; then
#   echo "1" > $count_file
# fi
PTY_ID=`echo $TTY | sed 's/\/dev\/pts\///g' | xargs`

# Increment the counter at every new terminal session
# if [[ -f /tmp/script_running ]]; then
  # session_count=$(($(cat $count_file) + 1))
  # echo $session_count > $count_file
# fi
LOG_FILE=/tmp/log-collector/session_$PTY_ID.log
SOCKET_PATH='/home/kali/.cyber-range-collector/cyber-range-collector.sock'
# echo "LOG FILE: " $LOG_FILE


# Code to run the script, capture the output of commands along with timestamps, and logs them to a file specified by /tmp/log-collector/session_$session_count.log.
if [[ -z "$SCRIPT_RUN" ]] && [ -f /tmp/script_running ]; then
export SCRIPT_RUN=1
# script -f  >(while read; do date +"%T.%3N";echo -n "$REPLY";done >> /tmp/log-collector/session_$session_count.log)
script -q -f  >(while read; do date +"%T.%3N";echo -n "$REPLY";done >> $LOG_FILE)
# script -f -O $LOG_FILE
fi


PREV_COMMAND=""
FIRST_LINE=3


# Hook which executes before every command. It collect each command
preexec() {
    if [ -f /tmp/script_running ]; then
      # When the script is executed, the pty is increased by one
      SCRIPT_LOG_FILE=/tmp/log-collector/session_$((PTY_ID - 1)).log

      CURRENT_SCRIPT_LINE_FILE=/tmp/log-collector/session_line_$((PTY_ID - 1)).count
      # At the first command creates the file, then takes the subset of lines
      if [ ! -e $CURRENT_SCRIPT_LINE_FILE ]; then
        echo $FIRST_LINE > $CURRENT_SCRIPT_LINE_FILE
        PREV_COMMAND=${1}
      else 
        if [ -e $SCRIPT_LOG_FILE ]; then
          NUM_LINES=`cat $SCRIPT_LOG_FILE | wc -l`
          # Send cli logs
          PREVIOUS=`cat $CURRENT_SCRIPT_LINE_FILE|xargs`
          TMP_FILE=/tmp/count_$RANDOM.txt
          sed -n "${PREVIOUS},${NUM_LINES}p" $SCRIPT_LOG_FILE > $TMP_FILE


          python send_cli_logs.py $((PTY_ID -1)) $PREV_COMMAND $TMP_FILE
          rm $TMP_FILE

          # $SCRIPT_LOG_FILE `cat $CURRENT_SCRIPT_LINE_FILE|xargs` $NUM_LINES
          echo $NUM_LINES > $CURRENT_SCRIPT_LINE_FILE
          PREV_COMMAND=${1}
          fi
      fi
      # if [ "$NUM_LINES" -gt $FIRST_LINE ]; then

      # fi
      # Copy the content in another file

      
        # if [[ ! -e $ ]] && [ -f /tmp/script_running ]; then
        #   echo "1" > $count_file
        # fi
        #   echo "Take count previous"

        #   # json_data=`jq -n --arg session_id "$session_count" --arg action stop '{session_id: $session_id, action: $action}'`
        #   # echo -n $json_data | socat - UNIX-CONNECT:"$SOCKET_PATH"
        #   # echo "" > $SOCKET_PATH
        #   # echo "" > $LOG_FILE
        # fi

        # PREV_COMMAND=${1}
        # echo "Start acquisition"
        # json_data=`jq -n --arg session_id "$session_count" --arg action start --arg command "${1}" '{session_id: $session_id, action: $action, command: $command}'`
        # echo $json_data
        # echo -n $json_data | socat - UNIX-CONNECT:"$SOCKET_PATH"

        # json_data=`jq -n --arg session_id "$session_count" --arg command "$1" '{session_id: $session_id, command: $command}'`
        # echo $json_data
        # echo $1 >> /tmp/log-collector/command_list$session_count.txt
    fi
}


# postexec() {
#   command_output=$(eval "$1")
#   command=$1
# }

# Set PROMPT_COMMAND to execute the postexec function after each command
PROMPT_COMMAND='postexec'
# precmd_functions+=(postexec)

