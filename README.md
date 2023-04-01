# CyberRange-Collector
This tool stores the input and output of all commands executed from each terminal session of the virtual machine. It also collects screenshots taken each  second and it produces a JSON file as output which contains all those informations. 

## Getting Started
### Prerequisites
First of all you have to install the dependencies so go into the project directory and type:
```shell
pip install -r requirements.txt
```

You need to have: 
* Scrot
* Script
* Python
* xdotool
* bc

Before running the tool you need to edit the *.zshrc* file by adding this code (substituting */directory-of-the-tool/* with your tool directory):
```shell
source /directory-of-the-tool/CyberRange-Collector/config/script-log.sh
```
### Start Logging
To start logging you need to open a terminal session in the folder where the file *log_tool.sh* is and type
```shell
source log_tool.sh -start
```
From now on, all terminal sessions will be logged and screenshots will be taken every 1 second. 
If you want to log terminal sessions with another screenshot rate you have to type:
```shell
source log_tool.sh -start -rate 10
```
From now on, all terminal sessions will be logged and screenshots will be taken with a rate of 10 screenshots/second.
If you don't want to take screenshots you have to type:
```shell
source log_tool.sh -start -noscreen
```
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
...}]}
}
```
You can find this JSON file at this path: `/home/script_directory/log/JSON`.
### Authors
* Marco Longobardi
* Manuele Toscano

