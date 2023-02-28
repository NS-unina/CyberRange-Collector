#!/bin/bash
scrot -u -d 1 $(xdotool getactivewindow getwindowname | tr -d '/"\\:*?<>|~' | sed 's/ //g')_%Y-%m-%d-%H:%M:%S.png
