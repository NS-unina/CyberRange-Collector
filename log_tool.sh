#!/bin/zsh

if [ "$1" == "-start" ]; then
rm ./*.png
touch /tmp/script_running
if [ -d ./screen ];
then
else
mkdir screen
fi
if [ -d ./logs ];
then
else
mkdir logs
fi
nohup zsh -c "while [ -f /tmp/script_running ]; do
source scrot_script.sh
done" &
elif [ "$1" == "-stop" ]; then
rm /tmp/script_running
rm /tmp/.zsh_session_count
python elab_JSON.py
else
echo "Nessuna opzione fornita"
fi
