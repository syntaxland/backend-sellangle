# user_profile/tasks.py
import random
import string
from datetime import datetime, timedelta
from django.utils import timezone

from celery import shared_task
from django.contrib.auth import get_user_model

User = get_user_model()


def generate_security_code():
    return ''.join(random.choices(string.digits, k=4))


@shared_task
def deactivate_inactive_users_every_six_months():
    six_months_ago = timezone.now() - timedelta(days=180)
    # six_months_ago = timezone.now() - timedelta(minutes=1)
    inactive_users = User.objects.filter(last_login__lte=six_months_ago)

    for user in inactive_users:
        user.user_is_not_active = True
        user.save()

    print("Inactive users deactivated.")


@shared_task
def delete_unverified_users_after_one_hour():
    one_hour_ago = timezone.now() - timedelta(hours=24)
    unverified_users = User.objects.filter(
        is_verified=False,
        is_staff=False,
        is_superuser=False,
        created_at__lte=one_hour_ago
    )

    unverified_users_count = unverified_users.count()
    unverified_users.delete()

    print(f"Deleted {unverified_users_count} unverified users.")


# venv\Scripts\activate.bat 
# python manage.py shell
# from user_profile.tasks import deactivate_inactive_users_every_six_months
# deactivate_inactive_users_every_six_months.delay()

"""
sudo service redis-server start 
sudo service redis-server status 
redis-cli ping
redis-server 
sudo service redis-server restart 
celery -A backend_drf.celery worker --pool=solo -l info  
(Windows)
celery -A backend_drf.celery worker --loglevel=info (Unix) 
celery -A backend_drf.celery beat --loglevel=info 
"""
