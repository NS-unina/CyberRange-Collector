#!/bin/bash
CYBER_RANGE_COLLECTOR_PATH=~/.cyber-range-collector
SCREENSHOT_PATH=${CYBER_RANGE_COLLECTOR_PATH}/screenshots
sleep $1
WIN_NAME=`xdotool getactivewindow getwindowname | tr -d '/"\\:*?<>|~' | sed 's/ //g'`
IMAGE_PATH="${SCREENSHOT_PATH}/${WIN_NAME}_$(date '+%Y-%m-%d-%H:%M:%S.%3N').png"
scrot -u ${IMAGE_PATH}
python ${CYBER_RANGE_COLLECTOR_PATH}/send_screen.py ${WIN_NAME} ${IMAGE_PATH}