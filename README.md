# CyberRange-Collector

This tool collects the input and output of all commands executed from each terminal session and screenshots taken each 10 seconds. It produces a JSON file as output which contains all those informations. 

## Prerequisites
Before running the tool you need to edit the *.zshrc* file by adding this code:
```shell
if [[ -z "$SCRIPT_RUN" ]] && [ -f /tmp/script_running ]; then
export SCRIPT_RUN=1
script -f $tty >(while read; do date +"%T.%3N";echo -n "$REPLY";done >> /home/nome_host/Documenti/script/log/session_$$.log)
fi
trap 'nohup script -f >(while read;do date +"%T.%3N";echo "$REPLY";done >> /home/nome_host/Documenti/script/log) 2>&1 & disown' EXIT
```
## Authors
* Marco Longobardi
* Manuele Toscano

