# CyberRange-Collector
This tool stores the input and output of all commands executed from each terminal session of the virtual machine. It also collects screenshots taken each 10 seconds and it produces a JSON file as output which contains all those informations. 

## Getting Started
### Prerequisites
Before running the tool you need to edit the *.zshrc* file by adding this code:
```shell
if [[ -z "$SCRIPT_RUN" ]] && [ -f /tmp/script_running ]; then
export SCRIPT_RUN=1
script -f $tty >(while read; do date +"%T.%3N";echo -n "$REPLY";done >> /home/host_name/Documenti/script/log/session_$$.log)
fi
trap 'nohup script -f >(while read;do date +"%T.%3N";echo "$REPLY";done >> /home/host_name/Documenti/script/log) 2>&1 & disown' EXIT
```
### Start Logging
To start logging you need to open a terminal session in the folder where the file *log_tool.sh* is and type
```shell
source log_tool.sh -start
```
From now on, all terminal sessions will be logged and screenshots will be taken every 10 seconds. 
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
### Authors
* Marco Longobardi
* Manuele Toscano

