# marketplace/tasks.py
import random
import string
from datetime import datetime, timedelta, timezone
from rest_framework import status
from rest_framework.response import Response

from celery import shared_task
from .models import (PostPaidAd, 
                    PostFreeAd,
                      AdChargeTotal
                      )
from credit_point.models import CreditPoint, AdChargeCreditPoint
from django.db import transaction
from django.db.models import Sum, F
from django.contrib.auth import get_user_model

User = get_user_model()


def generate_ad_charge_id(): 
    letters_and_digits = string.ascii_uppercase + string.digits
    return 'CHG'+''.join(random.choices(letters_and_digits, k=16))


@shared_task
def charge_ad():
    active_ads = PostPaidAd.objects.filter(expiration_date__gt=datetime.now())

    for ad in active_ads:
        ad_charges_hourly = 1.2  # cps per hr
        charge_hours = 1 # hrs
        
        PostPaidAd.objects.filter(id=ad.id).update(
            ad_charges=F('ad_charges') + ad_charges_hourly,
            ad_charge_hours=F('ad_charge_hours') + charge_hours
        ) 

    return 'Active ads found and charged:', len(active_ads)


@shared_task
def get_total_ad_charge():
    sellers = User.objects.filter(
        paid_ad_seller__expiration_date__gt=datetime.now(),
        paid_ad_seller__ad_charges__gt=0
    ).distinct()

    for seller in sellers:
        total_ad_charges = PostPaidAd.objects.filter(seller=seller, ad_charges__gt=0).aggregate(Sum('ad_charges'))['ad_charges__sum'] or 0
        total_ad_charge_hours = PostPaidAd.objects.filter(seller=seller, ad_charges__gt=0).aggregate(Sum('ad_charge_hours'))['ad_charge_hours__sum'] or 0

        total_ad_charge = AdChargeTotal.objects.filter(seller=seller).first()
        if total_ad_charge:
            AdChargeTotal.objects.filter(seller=seller).update(
                total_ad_charges=F('total_ad_charges') + total_ad_charges,
                total_ad_charge_hours=F('total_ad_charge_hours') + total_ad_charge_hours
            )
        else:
            AdChargeTotal.objects.create(
                seller=seller,
                total_ad_charges=total_ad_charges,
                total_ad_charge_hours=total_ad_charge_hours,
                total_ad_charge_id=generate_ad_charge_id(),
                timestamp=datetime.now()
            )

    return 'Total ad charges and hours calculated and saved for sellers:', len(sellers)


@shared_task
def deduct_total_ad_charge_from_cps():
    ad_charges_total = AdChargeTotal.objects.filter(
        total_ad_charges__gt=0,
    )

    with transaction.atomic():
        for total_ad_charge in ad_charges_total:
            try:
                credit_point = CreditPoint.objects.get(user=total_ad_charge.seller)
                credit_point_balance = credit_point.balance

                if credit_point_balance < total_ad_charge.total_ad_charges:
                    # send_seller_insufficient_cps_bal_email()
                    # send_seller_insufficient_cps_bal_msg()
                    print(f'Insufficient balance for seller {total_ad_charge.seller.username}')
                    continue

                CreditPoint.objects.filter(user=total_ad_charge.seller).update(
                    balance=F('balance') - total_ad_charge.total_ad_charges
                )

                credit_point = CreditPoint.objects.get(user=total_ad_charge.seller)
                cps_new_bal = credit_point.balance

                AdChargeCreditPoint.objects.create(
                    user=total_ad_charge.seller,
                    cps_amount=total_ad_charge.total_ad_charges,
                    old_bal=credit_point_balance,
                    new_bal=cps_new_bal, 
                    ad_charge_cps_id=generate_ad_charge_id(),
                    is_success=True,
                )

                AdChargeTotal.objects.filter(
                    seller=total_ad_charge.seller, 
                                             ).update(
                    total_ad_charges=0,
                    total_ad_charge_hours=0
                )

                PostPaidAd.objects.filter(
                    seller=total_ad_charge.seller, 
                    ad_charges__gt=0
                    ).update(
                    ad_charges=0,
                    ad_charge_hours=0
                )

            except CreditPoint.DoesNotExist:
                print(f'CreditPoint not found for seller {total_ad_charge.seller.username}')

    return 'Total ad charges deducted from seller credit points successfully.'

       

@shared_task
def delete_expired_ads():
    threshold_date = datetime.now() - timedelta(seconds=100)
    # threshold_date = datetime.now() - timedelta(days=7)

    expired_paid_ads = PostPaidAd.objects.filter(
        expiration_date__lte=threshold_date,
        ad_charges=0
    )

    expired_free_ads = PostFreeAd.objects.filter(
        expiration_date__lte=threshold_date,
    )

    expired_paid_ads.delete()
    expired_free_ads.delete()

    return 'Total deleted expired paid ads:', len(expired_paid_ads) 



"""
celery -A backend_drf.celery worker --pool=solo -l info 
(Windows)
celery -A backend_drf.celery worker --loglevel=info (Unix) 
celery -A backend_drf.celery beat --loglevel=info 
"""
