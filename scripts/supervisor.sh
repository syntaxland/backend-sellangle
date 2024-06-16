#!/bin/bash

# Check if Supervisor is installed
if ! command -v supervisorctl &> /dev/null; then
    echo "Supervisor is not installed. Installing Supervisor..."
    sudo apt update
    sudo apt install supervisor -y

    # Check if installation was successful
    if [ $? -ne 0 ]; then
        echo "Failed to install Supervisor. Exiting."
        exit 1
    fi

    # Start Supervisor service
    sudo service supervisor start
fi

# Check if Supervisor is running
if ! sudo service supervisor status > /dev/null; then
    echo "Supervisor is not running. Starting Supervisor..."
    sudo service supervisor start
fi

SUPERVISOR_CONFIG_DIR="/etc/supervisor/conf.d/"
LOG_DIR="/home/ubuntu/backend-sellangle/logs/celery/"

# Ensure log directories exist
sudo mkdir -p "$LOG_DIR"
sudo mkdir -p "$SUPERVISOR_CONFIG_DIR"

# Reread and update Supervisor configuration
sudo supervisorctl reread 
sudo supervisorctl update

# Start or restart Celerybeat
sudo supervisorctl restart celerybeat 

# Start or restart Celery
sudo supervisorctl restart celery 

# Check Supervisor status after restarting services
sudo service supervisor status
