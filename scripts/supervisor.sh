# scripts/supervisor.sh

#!/usr/bin/bash

# sudo supervisorctl reread
# sudo supervisorctl update
# sudo supervisorctl start celerybeat
# sudo supervisorctl start celery

#!/bin/bash

SUPERVISOR_CONFIG_DIR="/etc/supervisor/conf.d/"
LOG_DIR="/home/ubuntu/backend-sellangle/logs/celery/"

# Reread and update Supervisor configuration
sudo supervisorctl reread
sudo supervisorctl update

# Start or restart Celerybeat
sudo supervisorctl restart celerybeat 

# Start or restart Celery
sudo supervisorctl restart celery 

# Ensure log directories exist
sudo mkdir -p "$LOG_DIR"

sudo mkdir -p "$SUPERVISOR_CONFIG_DIR"

# Check Supervisor status
# sudo service supervisor status
