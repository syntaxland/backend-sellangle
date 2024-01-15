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
        receivers = [user.email for user in User.objects.all()]
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

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def send_email_to_all_users(request):
#     if request.method == 'POST':
#         subject = request.data.get('subject')
#         message = request.data.get('message')
#         print("\nEmail subject:", subject)

#         if not subject or not message:
#             return Response({'error': 'Subject and message are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
#         sender_name = settings.EMAIL_SENDER_NAME
#         sender_email = settings.EMAIL_HOST_USER
#         receivers = [user.email for user in User.objects.all()]
#         print("Receivers:", receivers)

#         # Email Sending API Config
#         configuration = sib_api_v3_sdk.Configuration()
#         configuration.api_key['api-key'] = settings.SENDINBLUE_API_KEY
#         api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

#         # Sending email
#         print("\nSending email ...")
#         html_content = message
#         sender = {"name": sender_name, "email": sender_email}
#         # to = [{"email": receiver} for receiver in receivers]
#         to = [{"email": receiver, "name": User.objects.get(email=receiver).first_name} for receiver in receivers]
#         send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
#             to=to,
#             html_content=html_content,
#             sender=sender,
#             subject=subject
#         )
        
#         try:
#             api_response = api_instance.send_transac_email(send_smtp_email)
#             print("\nEmail sent!")
#         except ApiException as e:
#             return Response({'error': 'Error sending email.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         # Create messages for each receiver
#         print("\nSaving email ...")
#         for receiver in receivers:
#             email = SendEmailMessage.objects.create(
#                 sender_user=request.user,
#                 receiver_user=User.objects.get(email=receiver),
#                 subject=subject,
#                 message=message
#             )
#         print("\nEmail saved!")
#         return Response({'detail': 'Email sent successfully.'}, status=status.HTTP_201_CREATED)

#     return Response({'detail': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)



# @api_view(['POST'])
# # @permission_classes([IsAuthenticated, IsAdminUser])
# @permission_classes([IsAuthenticated])  
# def send_email_to_all_users(request):
#     data = request.data
#     if request.method == 'POST':
#         subject = request.data.get('subject')
#         message = request.data.get('message')

#         if not subject or not message:
#             return Response({'error': 'Subject and message are required.'}, status=status.HTTP_400_BAD_REQUEST)

        
        
#         # sender_email = 'grammarpoint2@gmail.com'
#         sender_email = settings.EMAIL_HOST_USER  
#         sender_user = request.user  
#         # receivers = [user.email for user in User.objects.all()]
#         receivers = [receiver_user.email for receiver_user in User.objects.all()]
#         # first_names = [user.first_name for user in User.objects.all()]
#         # Email Sending API Config
#         configuration = sib_api_v3_sdk.Configuration()
#         configuration.api_key['api-key'] = settings.SENDINBLUE_API_KEY
#         api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
#         # Sending email
#         subject = subject
#         print("\nSending email ...")
#         first_name = data['first_name'].title() if data.get('first_name') else 'User'
#         html_content = message
#         sender_name = settings.EMAIL_SENDER_NAME
#         # sender_email = sender
#         # sender = sender
#         sender = {"name": sender_name, "email": sender_email}
#         to = [{"email": receivers, "name": first_name}]
#         # to = receiver
#         send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
#             to=to,
#             html_content=html_content, 
#             sender=sender,
#             subject=subject
#         )
#         try:
#             api_response = api_instance.send_transac_email(send_smtp_email)
#             print("\nEmail sent...")
#         except ApiException as e:
#             print(e)     
            
#         print("\Saving email ...")
#         # Create messages for each receiver
#         for receiver_user in receivers:
#             email_message = SendEmailMessage.objects.create(
#                 sender_user=sender_user,
#                 receiver_user=receiver_user,
#                 subject=subject,
#                 message=message
#             )

#             # serializer = SendEmailSerializer(email_message, many=True)
#             # return Response(serializer.data, status=status.HTTP_201_CREATED)
#             return Response({"detail": "Email sent to all users."}, status=status.HTTP_201_CREATED)
#         else:
#             return Response({'detail': 'You are not authorized.'}, 
#                             status=status.HTTP_403_FORBIDDEN)
#     else:
#         return Response(status=status.HTTP_400_BAD_REQUEST)



# @api_view(['POST'])
# @permission_classes([AllowAny])
# def send_email_otp(request):
#     data=request.data
#     serializer = EmailOTPSendSerializer(data=data)
#     if serializer.is_valid():
#         email = serializer.validated_data['email']
#         first_name = serializer.validated_data['first_name']
        
#         try:
#             # Send email OTP
#             email_otp, created = EmailOtp.objects.get_or_create(email=email)
#             # if not created:
#             email_otp.generate_email_otp()
           
#             # Email Sending API Config
#             configuration = sib_api_v3_sdk.Configuration()
#             configuration.api_key['api-key'] = settings.SENDINBLUE_API_KEY
#             api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
#             # Sending email
#             subject = "OTP Email Verification"
#             print("\nSending email OTP...")
#             first_name = data['first_name'].title() if data.get('first_name') else 'User'
#             html_content = f"""
#                 <!DOCTYPE html>
#                 <html>
#                 <head>
#                     <title>OTP Email Verification</title>
#                 </head>
#                 <body>
#                     <p>Dear {first_name.title()},</p>
#                     <p>Thank you for signing up with our service.
#                     To complete your registration, please use the OTP provided below:</p><br/>
#                     <h2>OTP: {email_otp.email_otp}</h2><br/>
#                     <p>This OTP is valid for 30 minutes.</p>
#                     <p>If you didn't request this verification email, please ignore it.</p>
#                     <p>Best regards,<br>McdofGlobal Team</p>
#                 </body>
#                 </html>
#             """ 
#             sender_name = settings.EMAIL_SENDER_NAME
#             sender_email = settings.EMAIL_HOST_USER
#             sender = {"name": sender_name, "email": sender_email}
#             to = [{"email": email, "name": first_name}]
#             send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
#                 to=to,
#                 html_content=html_content, 
#                 sender=sender,
#                 subject=subject
#             )
#             try:
#                 api_response = api_instance.send_transac_email(send_smtp_email)
#                 print('\nOTP sent:', email_otp.email_otp)
#             except ApiException as e:
#                 print(e)

#             return Response({'detail': 'Email verification OTP sent successfully.'}, status=status.HTTP_200_OK)
#         except EmailOtp.DoesNotExist:
#             return Response({'detail': 'User not found. Please register again.'}, status=status.HTTP_400_BAD_REQUEST)
#     else:
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def send_email_to_all_users(request):
#     try:
#         subject = request.data.get('subject')
#         message = request.data.get('message')

#         if not subject or not message:
#             return Response({'error': 'Subject and message are required.'}, status=400)

#         sender_email = 'your@email.com'  
#         receiver_emails = [user.email for user in User.objects.all()]

#         try:
#             # Send email OTP
#             email_otp, created = EmailOtp.objects.get_or_create(email=email)
#             # if not created:
#             email_otp.generate_email_otp()
           
#             # Email Sending API Config
#             configuration = sib_api_v3_sdk.Configuration()
#             configuration.api_key['api-key'] = settings.SENDINBLUE_API_KEY
#             api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
#             # Sending email
#             subject = "OTP Email Verification"
#             print("\nSending email OTP...")
#             first_name = data['first_name'].title() if data.get('first_name') else 'User'
#             html_content = f"""
#                 <!DOCTYPE html>
#                 <html>
#                 <head>
#                     <title>OTP Email Verification</title>
#                 </head>
#                 <body>
#                     <p>Dear {first_name.title()},</p>
#                     <p>Thank you for signing up with our service.
#                     To complete your registration, please use the OTP provided below:</p><br/>
#                     <h2>OTP: {email_otp.email_otp}</h2><br/>
#                     <p>This OTP is valid for 30 minutes.</p>
#                     <p>If you didn't request this verification email, please ignore it.</p>
#                     <p>Best regards,<br>McdofGlobal Team</p>
#                 </body>
#                 </html>
#             """ 
#             sender_name = settings.EMAIL_SENDER_NAME
#             sender_email = settings.EMAIL_HOST_USER
#             sender = {"name": sender_name, "email": sender_email}
#             to = [{"email": email, "name": first_name}]
#             send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
#                 to=to,
#                 html_content=html_content, 
#                 sender=sender,
#                 subject=subject
#             )
#             try:
#                 api_response = api_instance.send_transac_email(send_smtp_email)
#                 print('\nOTP sent:', email_otp.email_otp)
#             except ApiException as e:
#                 print(e)

#             return Response({'message': 'Emails sent successfully.'}, status=200)
#         except EmailOtp.DoesNotExist:
#                 return Response({'detail': 'User not found. Please register again.'}, status=status.HTTP_400_BAD_REQUEST)

#     except Exception as e:
#         return Response({'error': str(e)}, status=500)

