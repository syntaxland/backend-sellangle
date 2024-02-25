# support/tasks.py
from celery import shared_task
from support.models import SupportTicket, SupportResponse
from send_email.send_email_sendinblue import send_email_sendinblue
from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task
def close_resolved_tickets():
    threshold_date = timezone.now() - timedelta(days=7)
    # threshold_date = timezone.now() - timedelta(minutes=1)
    
    resolved_tickets_users = User.objects.filter(
        support_response_user__created_at__lte=threshold_date
    ).distinct()
    
    try:
        for user in resolved_tickets_users:
            user_tickets = SupportTicket.objects.filter(
                user=user,
                is_closed=False,
                created_at__lte=threshold_date,
            )

            for ticket in user_tickets:
                response_gt_7_days = SupportResponse.objects.filter(
                    support_ticket=ticket,
                    created_at__lte=threshold_date,
                ).exists()

                if response_gt_7_days:
                    ticket.is_closed = True
                    ticket.closed_at = timezone.now()
                    ticket.is_resolved = True
                    ticket.save()

                    # Send an email to notify the user that their ticket is now closed
                    subject = f"Your support ticket #{ticket.ticket_id} is now closed!"
                    first_name = user.first_name if user.first_name else 'User'
                    url = settings.SELLANGLE_URL
                    support_url =  f"{url}/support/ticket/{ticket.ticket_id}"
                    html_content = f"""
                        <!DOCTYPE html>
                        <html>
                        <head>
                            <title>Support Ticket Closed</title>
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
                                    background-color: #e53935; /* Red background color */
                                    color: #fff;
                                    padding: 10px 20px;
                                    text-decoration: none;
                                    border-radius: 5px; /* Rounded corners */
                                }}
                            </style>
                        </head>
                        <body>
                            <div class="container">
                                <div class="header">
                                    <h2>Support Ticket Closed</h2>
                                </div>
                                <div class="content">
                                    <p>Dear {first_name.title()},</p>
                                    <p>We have not heard back from you regarding your support ticket with <b>Ticket ID: #{ticket.ticket_id}</b> in the last 7 days. 
                                    We hope this means you have resolved your issue or question. 
                                    If you need continued support, please contact us or reply the support ticket using the reopen ticket button:</p>
                                    <p><a href="{support_url}" class="button">Reopen Ticket</a></p>
                                    <p>Best regards,</p>
                                    <p>Your Support Team</p>
                                </div>
                                <div class="footer">
                                    <p><em>This email was sent from an address that cannot accept incoming emails. 
                                    Please use the link above if you need to contact us about this same issue.</em></p>
                                    <p><em>{settings.COMPANY_NAME} is a subsidiary and registered trademark of {settings.PARENT_COMPANY_NAME}.</em></p>
                                </div>
                            </div>
                        </body>
                        </html>
                    """

                    to = [{"email": user.email, "name": user.first_name}]
                    send_email_sendinblue(subject, html_content, to)

    except Exception as e:
        print(str(e))

    return f"{len(resolved_tickets_users)} users with expired tickets processed successfully"


"""
redis-server
celery -A backend_drf.celery worker --pool=solo -l info 
(Windows)
celery -A backend_drf.celery worker --loglevel=info (Unix) 
celery -A backend_drf.celery beat --loglevel=info 
"""
