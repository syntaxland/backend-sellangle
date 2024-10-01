# marketplace/tasks.py
import random
import string
import base64 
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from io import BytesIO
from xhtml2pdf import pisa 

from celery import shared_task
from .models import (PostPaidAd, 
                    PostFreeAd,
                      AdChargeTotal
                      )

# from .views import generate_ad_charges_receipt_pdf                   
from credit_point.models import CreditPoint, CpsBonus, AdChargeCreditPoint
from promo.models import Referral
from send_message_inbox.models import SendMessageInbox
from send_email.send_email_sendinblue import send_email_sendinblue, send_email_with_attachment_sendinblue

from django.http import JsonResponse
from django.utils import timezone
from django.template.loader import get_template
from django.conf import settings
from django.db import transaction
from django.db.models import Sum, F
from django.contrib.auth import get_user_model

User = get_user_model()


def generate_ad_charge_id(): 
    letters_and_digits = string.ascii_uppercase + string.digits
    return 'CHG'+''.join(random.choices(letters_and_digits, k=16))


# @shared_task
# def charge_ad():
#     active_ads = PostPaidAd.objects.filter(expiration_date__gt=timezone.now())

#     for ad in active_ads:
#         ad_charges_hourly = 1.2  # cps per hr
#         charge_hours = 1 # hrs
        
#         PostPaidAd.objects.filter(id=ad.id).update(
#             ad_charges=F('ad_charges') + ad_charges_hourly,
#             ad_charge_hours=F('ad_charge_hours') + charge_hours
#         ) 

#     return 'Active ads found and charged:', len(active_ads)


# @shared_task
# def get_total_ad_charge():
#     sellers = User.objects.filter(
#         paid_ad_seller__expiration_date__gt=timezone.now(),
#         paid_ad_seller__ad_charges__gt=0
#     ).distinct()

#     for seller in sellers:
#         total_ad_charges = PostPaidAd.objects.filter(seller=seller, ad_charges__gt=0).aggregate(Sum('ad_charges'))['ad_charges__sum'] or 0
#         total_ad_charge_hours = PostPaidAd.objects.filter(seller=seller, ad_charges__gt=0).aggregate(Sum('ad_charge_hours'))['ad_charge_hours__sum'] or 0

#         total_ad_charge = AdChargeTotal.objects.filter(seller=seller).first()
#         if total_ad_charge:
#             AdChargeTotal.objects.filter(seller=seller).update(
#                 total_ad_charges=F('total_ad_charges') + total_ad_charges,
#                 total_ad_charge_hours=F('total_ad_charge_hours') + total_ad_charge_hours
#             )
#         else:
#             AdChargeTotal.objects.create(
#                 seller=seller,
#                 total_ad_charges=total_ad_charges,
#                 total_ad_charge_hours=total_ad_charge_hours,
#                 total_ad_charge_id=generate_ad_charge_id(),
#                 timestamp=timezone.now()
#             )

#     return 'Total ad charges and hours calculated and saved for sellers:', len(sellers)


@shared_task
def charge_ad():
    active_ads = PostPaidAd.objects.filter(expiration_date__gt=timezone.now())

    for ad in active_ads:
        ad_charges_hourly = 1.2  # cps per hr
        charge_hours = 1  # hrs
        
        PostPaidAd.objects.filter(id=ad.id).update(
            ad_charges=F('ad_charges') + ad_charges_hourly,
            ad_charge_hours=F('ad_charge_hours') + charge_hours
        ) 

    return 'Active ads found and charged:', len(active_ads)


@shared_task
def get_total_ad_charge():
    sellers = User.objects.filter(
        paid_ad_seller__expiration_date__gt=timezone.now(),
        paid_ad_seller__ad_charges__gt=0
    ).distinct()

    for seller in sellers:
        total_ad_charges = PostPaidAd.objects.filter(seller=seller, ad_charges__gt=0).aggregate(Sum('ad_charges'))['ad_charges__sum'] or 0
        total_ad_charge_hours = PostPaidAd.objects.filter(seller=seller, ad_charges__gt=0).aggregate(Sum('ad_charge_hours'))['ad_charge_hours__sum'] or 0

        total_ad_charge = AdChargeTotal.objects.filter(seller=seller).first()
        if total_ad_charge:
            AdChargeTotal.objects.filter(seller=seller).update(
                total_ad_charges=total_ad_charges,
                total_ad_charge_hours=total_ad_charge_hours
            )
        else:
            AdChargeTotal.objects.create(
                seller=seller,
                total_ad_charges=total_ad_charges,
                total_ad_charge_hours=total_ad_charge_hours,
                total_ad_charge_id=generate_ad_charge_id(),
                timestamp=timezone.now()
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

                # After deducting ad charges, apply the referral and followers bonuses
                implement_referral_cps_bonus(total_ad_charge.seller, total_ad_charge.total_ad_charges)
                implement_followers_cps_bonus(total_ad_charge.seller, total_ad_charge.total_ad_charges)

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

                # After deducting ad charges, apply the referral and followers bonuses
                implement_referral_cps_bonus(total_ad_charge.seller, total_ad_charge.total_ad_charges)
                implement_followers_cps_bonus(total_ad_charge.seller, total_ad_charge.total_ad_charges)

            except CreditPoint.DoesNotExist:
                print(f'CreditPoint not found for seller {user.username}')

    return 'Owed ad charges deducted from users successfully. Owed Users:', len(owed_users) 


def implement_referral_cps_bonus(user, total_ad_charges):
    try:
        referral = Referral.objects.get(referred_users=user)
        referrer = referral.referrer

        if not referrer:
            print(f"No referrer found for user {user.username}")
            return

        cps_bonus_amount = total_ad_charges * 0.10  # 10% of ad charges

        referrer_credit_point = CreditPoint.objects.get(user=referrer)
        old_balance = referrer_credit_point.balance
        new_balance = old_balance + cps_bonus_amount

        CpsBonus.objects.create(
            user=referrer,
            cps_bonus_type='Referral Bonus',
            cps_amount=cps_bonus_amount,
            cps_bonus_id=generate_ad_charge_id(),
            old_bal=old_balance,
            new_bal=new_balance,
            is_success=True,
        )

        referrer_credit_point.balance = new_balance
        referrer_credit_point.save()

        print(f"Referral bonus of {cps_bonus_amount} credited to referrer {referrer.username}")

    except Referral.DoesNotExist:
        print(f"No referral record found for user {user.username}")
    except CreditPoint.DoesNotExist:
        print(f"No credit point record found for referrer {referrer.username}")


def implement_followers_cps_bonus(user, total_ad_charges):
    try:
        followed_sellers = user.followed_sellers.all()
        if not followed_sellers:
            print(f"No followed sellers for user {user.username}")
            return

        cps_bonus_amount = total_ad_charges * 0.40  # 40% of ad charges
        cps_bonus_per_seller = cps_bonus_amount / followed_sellers.count()

        for seller in followed_sellers:
            seller_credit_point = CreditPoint.objects.get(user=seller)
            old_balance = seller_credit_point.balance
            new_balance = old_balance + cps_bonus_per_seller

            CpsBonus.objects.create(
                user=seller,
                cps_bonus_type='Followers',
                cps_amount=cps_bonus_per_seller,
                cps_bonus_id=generate_ad_charge_id(),
                old_bal=old_balance,
                new_bal=new_balance,
                is_success=True,
            )

            seller_credit_point.balance = new_balance
            seller_credit_point.save()

            print(f"Followers bonus of {cps_bonus_per_seller} credited to seller {seller.username}")

    except CreditPoint.DoesNotExist:
        print(f"No credit point record found for a followed seller")


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
def auto_reactivate_paid_ad():
    try:
        current_datetime = timezone.now()

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
            <p>We regret to inform you that one or more of your promoted ads couldn't be automatically reactivated due to insufficient CPS balance, 
            which is below <b>28.8 CPS</b>.
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


@shared_task
def delete_expired_ads():
    # threshold_date = timezone.now()() - timedelta(seconds=100)
    threshold_date = timezone.now() - timedelta(days=7)

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
def send_monthly_ad_billing_receipt_email():

    sellers = User.objects.filter(is_marketplace_seller=True)

    try:
        for user in sellers:
            print('user:', user)
            current_datetime = timezone.now()

            previous_month_start = datetime(current_datetime.year, current_datetime.month, 1) - relativedelta(months=1)
            previous_month_end = datetime(current_datetime.year, current_datetime.month, 1) - timedelta(days=1)
            ad_charges_receipt_month_formatted = previous_month_start.strftime('%m/%Y').strip()
            
            pdf_data = generate_ad_charges_receipt_pdf(user, ad_charges_receipt_month_formatted)

            ad_charges = AdChargeCreditPoint.objects.filter(
            user=user,
            created_at__range=(previous_month_start, previous_month_end),
            is_success=True
            ).values('created_at').annotate(total_ad_charges=Sum('cps_amount'))

            total_amount = ad_charges.aggregate(Sum('total_ad_charges'))['total_ad_charges__sum']
            formatted_total_amount = '{:,.2f}'.format(float(total_amount) if total_amount is not None else 0.0)
            print('formatted_total_amount:', formatted_total_amount)

            formatted_ad_charges_monthYear = previous_month_start.strftime('%B %Y').strip()
            print('formatted_ad_charges_monthYear:', formatted_ad_charges_monthYear)

            subject = f"Monthly Ad Billing for {formatted_ad_charges_monthYear}!"
            first_name = user.first_name if user.first_name else 'User'
            url = settings.SELLANGLE_URL
            billing_url =  f"{url}/billing"
            html_content = f"""
                <!DOCTYPE html>
                <html>
                    <head>
                        <title>Ad Billing for {ad_charges_receipt_month_formatted}</title>
                        <style>
                            body {{
                                font-family: Arial, sans-serif;
                                line-height: 1.6;
                                color: #333;
                            }}
                            .container {{
                                max-width: 600px;
                                margin: 0 auto;
                            }}
                            .header {{
                                background-color: #FF0000;;
                                color: white;
                                padding: 1em;
                                text-align: center;
                            }}
                            .content {{
                                padding: 1em;
                            }}
                            .footer {{
                                background-color: #f1f1f1;
                                padding: 1em;
                                text-align: center;
                            }}
                            .button {{
                                display: inline-block;
                                background-color: #007BFF; /* Red background color */
                                color: #fff;
                                padding: 10px 20px;
                                text-decoration: none;
                                border-radius: 5px; /* Rounded corners */
                            }}
                            </style>
                    </head>
                    <body>
                        <p>Dear {first_name},</p>
                        <p>We hope this message finds you well. Your monthly ad billing for {formatted_ad_charges_monthYear} is now available, totaling <b>{formatted_total_amount} CPS</b>.</p>
                        <p>Attached is a detailed billing receipt for your reference, demonstrating our commitment to transparency.</p>
                        <p>Review your billing details by clicking the following link: <a href="{billing_url}" class="button">Go to Billing Page</a></p>
                        <p>Your trust in our services is greatly appreciated. If you have any inquiries or need clarification, please don't hesitate to contact our support team.</p>
                        <p>Thank you for choosing SellAngle!</p>
                        <p>Best regards,<br>The SellAngle Team</p>
                    </body>
                </html>
            """

            to = [{"email": user.email, "name": user.first_name}]
            attachment_name = f"{ad_charges_receipt_month_formatted}_ad_charges_receipt.pdf"
            send_email_with_attachment_sendinblue(subject, html_content, to, attachment_data=pdf_data, attachment_name=attachment_name)

        return f"{len(sellers)} sellers sent monthly billing successfully"

    except Exception as e:
        print(str(e))


def generate_ad_charges_receipt_pdf(user, ad_charges_receipt_month_formatted):
    print('ad_charges_receipt_month_formatted:', ad_charges_receipt_month_formatted)

    try:
        month, year = ad_charges_receipt_month_formatted.split('/')
        month = int(month)
        print('month:', month)
        print('year:', year)

        start_date = datetime(int(year), month, 1)
        end_date = (start_date + relativedelta(months=1)) - timedelta(days=1)
        print('start_date:', start_date)
        print('end_date:', end_date)

        ad_charges = AdChargeCreditPoint.objects.filter(
            user=user,
            created_at__range=(start_date, end_date),
            is_success=True
        ).values('created_at').annotate(total_ad_charges=Sum('cps_amount')).order_by('created_at')

        total_amount = ad_charges.aggregate(Sum('total_ad_charges'))['total_ad_charges__sum']
        formatted_total_amount = '{:,.2f}'.format(float(total_amount) if total_amount is not None else 0.0)

        print('formatted_total_amount:', formatted_total_amount)
  
        context = {
            'user': user,
            'start_date': start_date.strftime('%B %d, %Y'),
            'end_date': end_date.strftime('%B %d, %Y'),
            'ad_charges': ad_charges,
            'account_id': 'Your Account ID Here',  
            'bill_status': 'Issued',
            'date_printed': timezone.now().strftime('%b %d, %Y'),  
            'formatted_total_amount': formatted_total_amount,
            'total_amount': total_amount,
            
        }
        # print('\ncontext:', context)

        template_path = 'marketplace/ad_charges_receipt.html'
        template = get_template(template_path)
        html = template.render(context)

        # Create PDF data
        pdf_content = BytesIO()
        pisa.CreatePDF(html, dest=pdf_content)
        pdf_content.seek(0)
        pdf_data = pdf_content.getvalue()
        pdf_content.close()
        return pdf_data

        # response = HttpResponse(content_type='application/pdf')
        # response['Content-Disposition'] = f'attachment; filename="{ad_charges_receipt_month_formatted}_ad_charges_receipt.pdf"'
        # pisa.CreatePDF(html, dest=response)
        # return response

    except AdChargeCreditPoint.DoesNotExist:
        return None



"""
sudo service redis-server start 
sudo service redis-server status 
redis-cli 
redis-server 
sudo service redis-server restart 
sudo service redis-server stop 
venv\Scripts\activate.bat 
celery -A backend_drf.celery worker --pool=solo -l info 
(Windows)
celery -A backend_drf.celery worker --loglevel=info (Unix) 
celery -A backend_drf.celery beat --loglevel=info 
"""
