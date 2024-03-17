# clean_instance.sh
#!/usr/bin/env bash

sudo rm -rf /home/ubuntu/backend-sellangle/* 

# Remove apt lock files if they exist
sudo rm /var/lib/dpkg/lock-frontend
sudo rm /var/cache/apt/archives/lock
sudo rm /var/lib/apt/lists/lock
