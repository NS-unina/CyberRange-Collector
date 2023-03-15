# CyberRange-Collector
This tool stores the input and output of all commands executed from each terminal session of the virtual machine. It also collects screenshots taken each  second and it produces a JSON file as output which contains all those informations. 

## Getting Started
### Prerequisites
You need to have: 
* Scrot
* Script
* Python
* xdotool

Before running the tool you need to edit the *.zshrc* file by adding this code (substituting */directory-of-the-tool/* with your tool directory):
```shell
# Path of the counter file
count_file=/tmp/.zsh_session_count

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
script -f $tty >(while read; do date +"%T.%3N";echo -n "$REPLY";done >> /directory-of-the-tool/logs/session_$session_count.log)
fi

# Hook which executes before every command 
preexec() {
    if [ -f /tmp/script_running ]; then
        echo $1 >> /directory-of-the-tool/logs/command_list$session_count.txt
    fi
}
```
### Start Logging
To start logging you need to open a terminal session in the folder where the file *log_tool.sh* is and type
```shell
source log_tool.sh -start
```
From now on, all terminal sessions will be logged and screenshots will be taken every 1 second. 
### Stop Logging
When you type
```shell
source log_tool.sh -stop
```
The tool stops logging and starts to elaborate the informations stored. It produces a JSON file which contains an entry for all terminal session started, with command input, output, working directory and timestamp, like this:
```JSON
{"host": 
{"session_name": 
[{"working_directory": "...",
"timestamp": "...",
"command": "...", 
"output": "..."}, 
{"working_directory": "...",
...}]}, 
"screenshots": []}
```
You can find this JSON file at this path: `/home/script_directory/log/JSON`.
### Authors
* Marco Longobardi
* Manuele Toscano

