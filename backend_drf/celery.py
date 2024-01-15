# backend_drf/celery.py
from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_drf.settings')

app = Celery('backend_drf')
app.conf.enable_utc = False

app.conf.update(timezone = 'Asia/Kolkata') 

app.config_from_object(settings, namespace='CELERY')

# Celery Beat Settings
app.conf.beat_schedule = {
    'calculate-at-n-time': {
        'task': 'sellers.tasks.send_mail_func',
        # 'schedule': crontab(hour=0, minute=46, ),
        'schedule': timedelta(seconds=10),
    }
    
}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


# Schedule the check_support_is_expired task to run every day at a specific time (adjust as needed).
app.conf.beat_schedule = {
    'check-support-is-expired': {
        'task': 'support.tasks.check_support_is_expired',
        # 'schedule': timedelta(seconds=10),
        'schedule': crontab(hour=0, minute=0),  # Run at midnight every day
    },
}
