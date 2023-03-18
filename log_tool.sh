#!/bin/zsh

if [ "$1" == "-start" ]; then
    rm ./*.png
    touch /tmp/script_running
    
    # Directory creation
    
    if [ -d ./screen ]; then
    	echo "'screen' directory already exists"
    else
        echo "Creating 'screen' directory..."
        mkdir screen
        echo "Directory created!"
    fi
    if [ -d ./logs ]; then
    	echo "'logs' directory already exists"
    else
        echo "Creating 'logs' directory..."
        mkdir logs
        echo "Directory created!"
    fi    
    
    # Option selection
    
    if [ "$2" == "-rate" ]; then
    	if [ "$3" != "" ]; then
            echo "Start collecting screenshots with rate: $3 screen/sec"
            export screen_rate=$(echo "scale=2; 1/$3" | bc) #sudo apt install bc
            nohup zsh -c "while [ -f /tmp/script_running ]; do
            scrot -u $(xdotool getactivewindow getwindowname | tr -d '/"\\:*?<>|~' | sed 's/ //g')_%Y-%m-%d-%H:%M:%S.png
            date
            sleep $screen_rate
            done" &
        else
            # Error output: missing params
            echo "You need to specify a valid rate argument"
            source log_tool.sh -stop
        fi    
    elif [ "$2" == "-noscreen" ]; then
    	# It starts without screenshots
    elif [ "$2" == "" ]; then
    	# Starting with a default rate
    	#nohup zsh -c "while [ -f /tmp/script_running ]; do
    	#source scrot_script.sh
    	#done" &
    	nohup zsh -c "while [ -f /tmp/script_running ]; do
    	scrot -u -d 1 $(xdotool getactivewindow getwindowname | tr -d '/"\\:*?<>|~' | sed 's/ //g')_%Y-%m-%d-%H:%M:%S.png
	done" &
    else
    	# Error: invalid option
    	echo "You need to specify a valid option"
        source log_tool.sh -stop
    fi
elif [ "$1" == "-stop" ]; then
    rm /tmp/script_running
    rm /tmp/.zsh_session_count
    python elab_JSON.py
elif [ "$1" == "-help" ]; then
    echo "Usage: source log_tool.sh [option]"
    echo "Options:"
    echo "    -start: start the logging tool with default screen rate"
    echo "    -stop: stop the logging tool and process the log data"
    echo "    -noscreen: start the logging tool without taking screenshots"
    echo "    -rate x: take x screenshots/seconds"
    echo "    -help: display this help message"
else
    echo "Nessuna opzione fornita"
fi
