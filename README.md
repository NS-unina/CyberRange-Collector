# CyberRange-Collector
## Prerequisiti
Prima di eseguire il tool bisogna modificare il file *.zshrc* aggiungendo tale codice:
```shell
if [[ -z "$SCRIPT_RUN" ]] && [ -f /tmp/script_running ]; then
export SCRIPT_RUN=1
script -f $tty >(while read; do date +"%T.%3N";echo -n "$REPLY";done >> /home/nome_host/Documenti/script/log/session_$$.log)
fi
trap 'nohup script -f >(while read;do date +"%T.%3N";echo "$REPLY";done >> /home/nome_host/Documenti/script/log) 2>&1 & disown' EXIT
```
In questo modo, ogni volta che si avvia una nuova sessione del terminale si valutano le due condizioni dell'if:
* La condizione `if [[ -z "$SCRIPT_RUN" ]]` controlla se la variabile d'ambiente "SCRIPT_RUN" è vuota;
* La condizione `if [ -f /tmp/script_running ]` controlla se il file "/tmp/script_running" esiste.

A questo punto si setta ad 1 la variabile d'ambiente per non rientrare nel ramo dell'if per la sessione in corso.

Si utilizza il tool `script` per avviare la registrazione della sessione del terminale. Esso esegue una nuova shell e registra tutto l'output su un file specificato come argomento. 

Il flag `-f` specifica il file su cui verrà registrato l'output e `$tty` viene utilizzato per ottenere il dispositivo TTY associato alla sessione corrente.

Con `>(while read; do date +"%T.%3N";echo -n "$REPLY";done >> /home/nome_host/Documenti/script/log/session_$$.log)` si effettua la redirezione di processo per eseguire un ciclo "while" che legge l'output della shell script e lo registra in un file di log. Il ciclo "while" utilizza la data corrente con il formato `%T.%3N` (ora, minuti, secondi e millisecondi) e `echo -n "$REPLY"` per registrare l'output della sessione corrente. Il file di log verrà salvato nella directory `/home/nome_host/Documenti/script/log` con il nome `session_$$.log`, dove `$$` rappresenta il PID (Process ID) della shell script corrente.

Il tool `script` smette di registrare quando da in input il comando `exit`, per questo motivo è stata inserita questa riga di codice:

`trap 'nohup script -f >(while read;do date +"%T.%3N";echo "$REPLY";done >> /home/nome_host/Documenti/script/log) 2>&1 & disown' EXIT`

in modo tale da far ripartire la registrazione quando si digita `exit`.

## log_tool.sh
```shell
#!/bin/zsh

if [ "$1" == "-start" ]; then
echo "STOP_SCRIPT=0" > /etc/log_tool/tool_variable
touch /tmp/script_running
nohup zsh -c "while [ -f /tmp/script_running ]; do
scrot -u -d 10 '%Y-%m-%d-%H:%M:%S.png'
done" &
elif [ "$1" == "-stop" ]; then
rm /tmp/script_running
python elab_JSON.py
mv *.png screen/
else
echo "Nessuna opzione fornita"
fi
```

Lo script si avvia utilizzando l'opzione `-start`, con la quale si setta a 0 la variabile d'ambiente e viene creato `script_running` (condizioni nell'if della sezione precedente) in modo che possa partire la registrazione delle sessioni. Si avvia, inoltre, `scrot` per effettuare gli screenshot ogni 10s. 

Lo script si ferma con l'opzione `-stop` con la quale si avvia lo script python per l'elaborazione dei file di log generati e vengono ricollocati tutti gli screen nella cartella indicata.

## elab_JSON.py
Script python per l'elaborazione dei file di log prodotti e la produzione di un file JSON con questa struttura:
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
