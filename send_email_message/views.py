from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .serializers import SendEmailSerializer  
from .models import  SendEmailMessage

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException 

from django.db.models import Q
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_email_to_all_users(request):
    if request.method == 'POST':
        subject = request.data.get('subject')
        message = request.data.get('message')
        print("\nEmail subject:", subject)

        if not subject or not message:
            return Response({'error': 'Subject and message are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        sender_name = settings.EMAIL_SENDER_NAME
        sender_email = settings.EMAIL_HOST_USER
        # receivers = [user.email for user in User.objects.all()]
        receivers = [user.email for user in User.objects.filter(user_is_not_active=False)]
        print("Receivers:", receivers)

        # user_first_names = [user.first_name for user in User.objects.all()]
        # interpolated_messages = [message.format(userFirstName=name) for name in user_first_names]
        
        # Email Sending API Config
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = settings.SENDINBLUE_API_KEY
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

        # Sending email
        print("\nSending email ...")
        html_content = message
        sender = {"name": sender_name, "email": sender_email}
        # to = [{"email": receiver} for receiver in receivers]
        to = [{"email": receiver, "name": User.objects.get(email=receiver).first_name} for receiver in receivers]
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=to,
            html_content=html_content,
            sender=sender,
            subject=subject
        )
        
        try:
            api_response = api_instance.send_transac_email(send_smtp_email)
            print("\nEmail sent!")
        except ApiException as e:
            return Response({'error': 'Error sending email.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Create messages for each receiver
        print("\nSaving email ...")
        for receiver in receivers:
            email = SendEmailMessage.objects.create(
                sender_user=request.user,
                receiver_user=User.objects.get(email=receiver),
                subject=subject,
                message=message
            )
        print("\nEmail saved!")
        return Response({'detail': 'Email sent successfully.'}, status=status.HTTP_201_CREATED)

    return Response({'detail': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST) 

