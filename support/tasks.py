# support/tasks.py
from celery import shared_task

from support.models import SupportTicket, SupportResponse

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

from datetime import timedelta

from django.utils import timezone
from django.conf import settings
from django.db.models import Max, F, OuterRef, Subquery
from django.db.models.functions import Coalesce
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task
def check_support_is_expired():
    try:
        # Calculate the threshold date (7 days ago)
        # threshold_date = timezone.now() - timedelta(days=7) 
        threshold_date = timezone.now() - timedelta(seconds=30) 

        # Subquery to get the last SupportResponse creation date for each SupportTicket
        last_support_message_created = SupportResponse.objects.filter(
            support_ticket=OuterRef('pk')
        ).order_by('-created_at').values('created_at')[:1]

        # # Get users with open support tickets older than 7 days 
        # users_with_expired_tickets = User.objects.filter(
        #     support_user__is_closed=False,  # Open tickets
        #     support_user__support_ticket__created_at__lte=threshold_date,  # Older than 7 days
        # ).distinct()  

        # Get users whose last SupportResponse creation date is lte threshold_date
        users_with_expired_tickets = User.objects.filter(
            support_user__is_closed=False,  # Open tickets
            support_user__support_ticket__created_at__lte=threshold_date,  # Older than 7 days
        ).annotate(
            last_support_message_created_at=Coalesce(Subquery(last_support_message_created), F('support_user__created_at'))
        ).filter(
            last_support_message_created_at__lte=threshold_date
        ).distinct()

        # Update and close the tickets for each user
        for user in users_with_expired_tickets:
            user_tickets = SupportTicket.objects.filter(
                user=user,
                is_closed=False,  # Open tickets
                support_ticket__created_at__lte=threshold_date,  # Older than 7 days
            )

            # Update and close each ticket
            for ticket in user_tickets:
                ticket.is_closed = True
                ticket.closed_at = timezone.now()
                ticket.save()

                # Send an email to notify the user that their ticket is now closed
                send_ticket_closed_email(user, ticket)

    except Exception as e:
        print(str(e))
    return f"{len(users_with_expired_tickets)} users with expired tickets processed successfully"


def send_ticket_closed_email(user, ticket):
    try:
        # Email Sending API Configuration
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = settings.SENDINBLUE_API_KEY
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

        # Sending email
        subject = f"Your support ticket #{ticket.ticket_id} is now closed"
        content = f"Dear {user.username},\n\nYour support ticket with ID #{ticket.ticket_id} has been closed. If you have any further questions or need assistance, please feel free to open a new ticket.\n\nBest regards,\nYour Support Team"
        sender = {"name": settings.PAYSOFTER_EMAIL_SENDER_NAME, "email": settings.EMAIL_HOST_USER}
        to = [{"email": user.email}]

        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=to,
            html_content=content,
            sender=sender,
            subject=subject
        )

        api_instance.send_transac_email(send_smtp_email)
    except ApiException as e:
        print(f"Error sending email: {str(e)}")
