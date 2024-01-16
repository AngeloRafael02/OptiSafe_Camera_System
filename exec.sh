#!/bin/bash

# Replace 'path_to_your_python_app' with the actual path to your Python application script.
APP_PATH="/opt/OptiSafe_Camera/main.py"
PID_FILE="/var/run/OptiSafe_Camera.pid"

start() {
    if [ -f $PID_FILE ]; then
        echo "The service is already running."
    else
        cd $APP_PATH
        source .venv/bin/activate
        nohup python3 $APP_PATH &> /dev/null &
        echo $! > $PID_FILE
        echo "Service started."
    fi
}

stop() {
    if [ -f $PID_FILE ]; then
        kill $(cat $PID_FILE)
        rm $PID_FILE
        deactivate
        echo "Service stopped."
    else
        echo "The service is not running."
    fi
}

restart() {
    stop
    start
}

update(){
    if [ -f $PID_FILE ]; then
        stop
        cd /opt/OptiSafe_Camera
        git pull --force
        start
    else
        cd /opt/OptiSafe_Camera
        git pull --force
    fi
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    update)
        update
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|update}"
esac