#!/usr/bin/bash 

sed -i 's/\[]/\["54.159.74.226"]/' /home/ubuntu/backend-sellangle/backend_drf/settings.py

python manage.py migrate 
python manage.py collectstatic
sudo service gunicorn restart
sudo service nginx restart 

#sudo tail -f /var/log/nginx/error.log
#sudo systemctl reload nginx
#sudo nginx -t
#sudo systemctl restart gunicorn
#sudo systemctl status gunicorn
#sudo systemctl status nginx

# Check the status
#systemctl status gunicorn

# Restart:
#systemctl restart gunicorn
#sudo systemctl status nginx
