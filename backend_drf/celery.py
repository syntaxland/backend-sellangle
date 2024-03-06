# # backend_drf/celery.py
from __future__ import absolute_import, unicode_literals
import os
from django.conf import settings
from celery import Celery
from celery.schedules import crontab
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_drf.settings') 

app = Celery('backend_drf') 
app.conf.enable_utc = False
app.conf.update(timezone =  'Africa/Lagos')  
app.config_from_object(settings, namespace='CELERY')

app.conf.beat_schedule = {
    'charge-ad-charges': {
        'task': 'marketplace.tasks.charge_ad',
        'schedule': timedelta(seconds=60),
        # 'schedule': timedelta(hours=1),
    },
    'get-total-ad-charge': {
        'task': 'marketplace.tasks.get_total_ad_charge',
        # 'schedule': crontab(hour=0, minute=0),  
        'schedule': timedelta(seconds=62),
    },
    'deduct-total-ad-charge-from-cps': {
        'task': 'marketplace.tasks.deduct_total_ad_charge_from_cps',
        # 'schedule': crontab(hour=0, minute=1),  
        'schedule': timedelta(seconds=100),
        # 'schedule': timedelta(hours=1),
    },
    'charge-owed-ads': {
        'task': 'marketplace.tasks.charge_owed_ads',
        # 'schedule': crontab(hour=0, minute=0),  
        'schedule': timedelta(seconds=15),
        # 'schedule': timedelta(hours=1),
    },
    'auto-reactivate-paid-ad': {
        'task': 'marketplace.tasks.auto_reactivate_paid_ad',
        'schedule': timedelta(seconds=45),
    },
    'delete-expired-ads': {
        'task': 'marketplace.tasks.delete_expired_ads',
        # 'schedule': crontab(hour=0, minute=0),  
        'schedule': timedelta(hours=1),
        # 'schedule': timedelta(minutes=10),
    },
    'send-monthly-ad-billing-receipt-email': {
        'task': 'marketplace.tasks.send_monthly_ad_billing_receipt_email',
        # 'schedule': crontab(minute=0, hour=2, day_of_month=1),
        # 'schedule': timedelta(seconds=420),
        'schedule': timedelta(minutes=180),
    },
    'close-resolved-tickets': {
        'task': 'support.tasks.close_resolved_tickets',
        'schedule': timedelta(seconds=10),
    },
} 

app.autodiscover_tasks()
