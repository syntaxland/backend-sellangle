#!/bin/bash

# Create Supervisor Configuration Directory
sudo mkdir -p /etc/supervisor/conf.d/ 
 
# Create Supervisor Log Directory
sudo mkdir -p /var/log/supervisor/ 

# Create Celery Log Directory
sudo mkdir -p /home/ubuntu/backend-sellangle/logs/celery/ 

# Create log files if they don't exist
sudo touch /home/ubuntu/backend-sellangle/logs/celery/worker-access.log 
sudo touch /home/ubuntu/backend-sellangle/logs/celery/beat-access.log 

# Set appropriate permissions for Celery log directory
sudo chown -R ubuntu:ubuntu /home/ubuntu/backend-sellangle/logs/celery/
sudo chmod -R 755 /home/ubuntu/backend-sellangle/logs/celery/

# Restart Supervisor to pick up changes
sudo service supervisor restart 

# Check Supervisor status after restarting services
sudo service supervisor status 
