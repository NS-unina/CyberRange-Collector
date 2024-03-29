#!/bin/zsh

if [ "$1" == "-start" ]; then
    rm  -f ./*.png
    # Added configuration to file .zshrc
    SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
    if grep -q "source $SCRIPT_DIR/config/script-log.sh" ~/.zshrc; then
    else
    echo "source $SCRIPT_DIR/config/script-log.sh" >> ~/.zshrc
    fi
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
            export screen_rate=$(echo "scale=2; 1/$3" | bc)
            nohup zsh -c "while [ -f /tmp/script_running ]; do
    	source scrot_script.sh $screen_rate
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
    	nohup zsh -c "while [ -f /tmp/script_running ]; do
    	source scrot_script.sh 1
    	done" &
    else
    	# Error: invalid option
    	echo "You need to specify a valid option"
        source log_tool.sh -stop
    fi
elif [ "$1" == "-stop" ]; then
    rm -f /tmp/script_running
    rm -f /tmp/.zsh_session_count
    python elab_JSON.py

elif [ "$1" == "-upload" ]; then
    python api-call.py

elif [ "$1" == "-help" ]; then
    echo "Usage: source log_tool.sh [option]"
    echo "Options:"
    echo "    -start: start the logging tool with default screen rate"
    echo "    -stop: stop the logging tool and process the log data"
    echo "    -noscreen: start the logging tool without taking screenshots"
    echo "    -rate x: take x screenshots/seconds"
    echo "    -help: display this help message"
else
    echo "No opt"
fi
