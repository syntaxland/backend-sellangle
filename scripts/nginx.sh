
#!/usr/bin/bash

sudo systemctl daemon-reload
sudo rm -f /etc/nginx/sites-enabled/default

sudo cp /home/ubuntu/backend-sellangle/nginx/nginx.conf /etc/nginx/sites-available/backend-sellangle
sudo ln -s /etc/nginx/sites-available/backend-sellangle /etc/nginx/sites-enabled/
#sudo nginx -t
sudo gpasswd -a www-data ubuntu
sudo systemctl restart nginx 

