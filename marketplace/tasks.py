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
from send_message_inbox.models import SendMessageInbox
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
                    PostPaidAd.objects.filter(
                    seller=total_ad_charge.seller, 
                    ad_charges__gt=0
                    ).update(
                    )
                    total_ad_charge.seller.ad_charge_is_owed=True
                    total_ad_charge.seller.save()

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
                    ad_charge_hours=0,
                )
                total_ad_charge.seller.ad_charge_is_owed=False
                total_ad_charge.seller.save()

            except CreditPoint.DoesNotExist:
                print(f'CreditPoint not found for seller {total_ad_charge.seller.username}')

    return 'Total ad charges deducted from seller credit points successfully.'

       

@shared_task
def charge_owed_ads():
    owed_users = User.objects.filter(ad_charge_is_owed=True)

    for user in owed_users:
        total_ad_charge = AdChargeTotal.objects.filter(seller=user).first()

        if total_ad_charge:
            try:
                credit_point = CreditPoint.objects.get(user=user)
                credit_point_balance = credit_point.balance
                insufficient_cps_balance = total_ad_charge.total_ad_charges

                if credit_point_balance < total_ad_charge.total_ad_charges:
                    # send_seller_insufficient_cps_bal_email(user)
                    send_seller_insufficient_cps_bal_msg(user, insufficient_cps_balance, credit_point_balance)
                    print(f'Insufficient balance for seller {user.username}')
                    continue

                # Deduct total_ad_charges from credit point balance
                CreditPoint.objects.filter(user=user).update(
                    balance=F('balance') - total_ad_charge.total_ad_charges
                )

                credit_point = CreditPoint.objects.get(user=user)
                cps_new_bal = credit_point.balance

                AdChargeCreditPoint.objects.create(
                    user=user,
                    cps_amount=total_ad_charge.total_ad_charges,
                    old_bal=credit_point_balance,
                    new_bal=cps_new_bal,
                    ad_charge_cps_id=generate_ad_charge_id(),
                    is_success=True,
                )

                AdChargeTotal.objects.filter(
                    seller=user,
                ).update(
                    total_ad_charges=0,
                    total_ad_charge_hours=0
                )

                PostPaidAd.objects.filter(
                    seller=user,
                    ad_charges__gt=0
                ).update(
                    ad_charges=0,
                    ad_charge_hours=0,
                )

                user.ad_charge_is_owed = False
                user.save()

            except CreditPoint.DoesNotExist:
                print(f'CreditPoint not found for seller {user.username}')

    return 'Owed ad charges deducted from users successfully. Owed Users:', len(owed_users) 


def send_seller_insufficient_cps_bal_msg(user, credit_point_balance, insufficient_cps_balance):
    
    # system_user, created = User.objects.get_or_create(username='system_user')

    formatted_outstanding_cps_amount = '{:,.2f}'.format(float(credit_point_balance))
    formatted_insufficient_cps_balance = '{:,.2f}'.format(float(insufficient_cps_balance))

    message_content = f"""
        <html>
        <head>
            <title>Insufficient CPS Balance</title>
        </head>
        <body>
            <p>Dear {user.username},</p>
            <p>Your ad charges of <b>{formatted_outstanding_cps_amount} CPS</b> owed couldn't be deducted due to insufficient credit point balance <b>({formatted_insufficient_cps_balance} CPS)</b> .</p>
            <p>Please fund your CPS wallet to continue using our services.</p>
            <p>Best regards,<br>The Support Team</p>
        </body>
        </html>
    """

    inbox_message = SendMessageInbox.objects.create(
        # sender=system_user,  
        receiver=user,
        subject="Insufficient CPS Balance (Ad Charges)",
        message=message_content,
        is_read=False,
    )

    inbox_message.msg_count += 1
    inbox_message.save()
    
    print(f"Notification sent to {user.username} about insufficient CPS balance.")


@shared_task
def delete_expired_ads():
    # threshold_date = datetime.now() - timedelta(seconds=100)
    threshold_date = datetime.now() - timedelta(days=7)

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


@shared_task
def auto_reactivate_paid_ad():
    try:
        current_datetime = datetime.now()

        expired_ads = PostPaidAd.objects.filter(is_auto_renewal=True, expiration_date__lt=current_datetime)

        for ad in expired_ads:
            user_credit_point = CreditPoint.objects.get(user=ad.seller)
            credit_point_balance = user_credit_point.balance
            # insufficient_cps_balance = 28.8
            if user_credit_point.balance < 28.8:
                send_auto_renewal_insufficient_cps_bal_msg(ad.seller, credit_point_balance)
                continue 

            with transaction.atomic():
                # ad.duration = ad.duration 
                ad.duration = '1 day' 
                ad.is_active = True
                ad.save()

        return f"Auto-reactivation completed. Reactivated {len(expired_ads)} expired paid ads."

    except Exception as e:
        return f"Error during auto-reactivation: {str(e)}"


def send_auto_renewal_insufficient_cps_bal_msg(user, credit_point_balance):
    # system_user, created = User.objects.get_or_create(username='system_user')
    formatted_insufficient_cps_balance  = '{:,.2f}'.format(float(credit_point_balance))
    # formatted_outstanding_cps_amount = '{:,.2f}'.format(float(insufficient_cps_balance))

    message_content = f"""
        <html>
        <head>
            <title>Insufficient CPS Balance</title>
        </head>
        <body>
            <p>Dear {user.username},</p>
            <p>We regret to inform you that one or more of your promoted ads couldn't be automatically reactivated due to insufficient CPS balance, which is below <b>28.8 CPS</b>.
              Your current credit point balance is <b>({formatted_insufficient_cps_balance} CPS)</b>.</p>
            <p>Please ensure your CPS wallet is funded to continue benefiting from our services.</p>
            <p>Best regards,<br>The Support Team</p>
        </body>
        </html>
    """

    inbox_message = SendMessageInbox.objects.create(
        # sender=system_user,  
        receiver=user,
        subject="Insufficient CPS Balance (Ad auto-renewal)",
        message=message_content,
        is_read=False,
    )

    inbox_message.msg_count += 1
    inbox_message.save()
    
    print(f"Notification sent to {user.username} about insufficient CPS balance.")


"""
celery -A backend_drf.celery worker --pool=solo -l info 
(Windows)
celery -A backend_drf.celery worker --loglevel=info (Unix) 
celery -A backend_drf.celery beat --loglevel=info 
"""
