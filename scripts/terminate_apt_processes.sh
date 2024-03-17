#!/bin/bash

# Check if any apt-get processes are running and terminate them
if pgrep -x "apt-get" >/dev/null; then
    echo "Terminating apt-get processes..."
    sudo killall apt-get
    sleep 5 # Wait for processes to terminate
else
    echo "No apt-get processes are running."
fi
