# scripts/supervisor.sh

#!/usr/bin/bash

sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start celerybeat
sudo supervisorctl start celery
