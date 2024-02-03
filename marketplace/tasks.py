# marketplace/tasks.py
import random
import string
from datetime import datetime, timedelta, timezone

# from celery import Celery
from celery import shared_task
from django.db.models import Sum
from django.db.models import F
from .models import PostPaidAd, AdCharge


def generate_ad_charge_id():
    letters_and_digits = string.ascii_uppercase + string.digits
    return 'CHG'+''.join(random.choices(letters_and_digits, k=16))


@shared_task
def charge_ad_charges():
    # Get all active ads
    active_ads = PostPaidAd.objects.filter(expiration_date__gt=timezone.now())

    # Charge 1 cps per hour for each active ad
    for ad in active_ads:
        ad_charges, created = AdCharge.objects.get_or_create(
            seller=ad.seller,
            paid_ad=ad,
        )

        # Calculate the charges based on the elapsed time since last charge
        elapsed_hours = (timezone.now() - ad_charges.timestamp).total_seconds() / 3600
        charges = elapsed_hours * 1  # 1 cps per hour

        # Update the charges in the AdCharge model
        AdCharge.objects.filter(pk=ad_charges.pk).update(
            ad_charges=F('ad_charges') + charges,
            timestamp=timezone.now(),
        )

    return 'Ad charges updated successfully'





"""
celery -A core.celery worker --pool=solo -l info 
(Windows)
celery -A core.celery worker --loglevel=info (Unix) 
celery -A core.celery beat --loglevel=info
"""
