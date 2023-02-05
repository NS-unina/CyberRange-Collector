#!/bin/zsh

if [ "$1" == "-start" ]; then
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
