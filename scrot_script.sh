#!/bin/bash
sleep $1
scrot -u "$(xdotool getactivewindow getwindowname | tr -d '/"\\:*?<>|~' | sed 's/ //g')_$(date '+%Y-%m-%d-%H:%M:%S.%3N').png"