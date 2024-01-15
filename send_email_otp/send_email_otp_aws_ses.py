import random
import boto3

from django_otp import devices_for_user 

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from .models import EmailOtp

User = get_user_model()


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def send_email_otp(request):
    user_email = "softglobal3@gmail.com"
    user_first_name = "chibuzo"
    # user_data = request.session.get('user_data')
    # if user_data:
    #     user_email = user_data.get('email')
    #     user_first_name = user_data.get('first_name')

    email_otp, created = EmailOtp.objects.get_or_create(email=user_email) 
    email_otp.generate_email_otp()
    # otp = email_otp.email_otp
    # print(otp)

    # Sending email using AWS SES
    ses_client = boto3.client(
        'ses',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION
    )

    subject = "OTP Email Verification"
    message = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>OTP Email Verification</title>
        </head>
        <body>
            <p>Dear {user_first_name.title()},</p>
            <p>Thank you for signing up with our service.
            To complete your registration, please use the OTP provided below:</p><br/>
            <h2>OTP: {email_otp.email_otp}</h2><br/>
            <p>This OTP is valid for 30 minutes.</p>
            <p>If you didn't request this verification email, please ignore it.</p>
            <p>Best regards,<br>Softglobal Team</p>
        </body>
        </html>
    """

    try:
        response = ses_client.send_email(
            Source=settings.EMAIL_HOST_USER,  
            Destination={
                'ToAddresses': [user_email],
            },
            Message={
                'Subject': {
                    'Data': subject,
                },
                'Body': {
                    'Text': {
                        'Data': message,
                    },
                }
            }
        )
        print(response)
        return Response({'detail': 'Email verification OTP sent successfully.'}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({'detail': 'Failed to send verification email'}, status=status.HTTP_400_BAD_REQUEST)


# # Helper function to generate OTP
# def generate_otp():
#     return str(random.randint(100000, 999999))

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def send_email_otp(request):
#     # email = request.data.get('email')
#     email = "syntaxland@gmail.com"
#     try:
#         otp_device = devices_for_user(EmailOtp, email=email).get()
#     except ObjectDoesNotExist:
#         otp_device = EmailOtp.objects.create(email=email)
#     else:
#         otp_device.generate_challenge()
#         otp_device.save()

#     sns = boto3.client('sns', region_name=settings.AWS_SNS_REGION)
#     sns.publish(
#         TopicArn=settings.AWS_SNS_TOPIC_ARN,
#         Message=f'Your OTP is: {otp_device.token()}',
#     )

#     return Response({'message': 'OTP sent successfully'})


@api_view(['POST'])
def verify_email_otp(request):
    email = request.data.get('email')
    otp_code = request.data.get('otp_code')

    try:
        otp_device = devices_for_user(EmailOtp, email=email).get()
    except ObjectDoesNotExist:
        return JsonResponse({'message': 'Invalid OTP'}, status=400)

    if not otp_device.verify(otp_code):
        return JsonResponse({'message': 'Invalid OTP'}, status=400)

    if otp_device.t() < timezone.now() - timezone.timedelta(minutes=15):
        return JsonResponse({'message': 'OTP has expired'}, status=400)

    otp_device.confirmed = True
    otp_device.save()

    return Response({'message': 'OTP verified successfully'})


@api_view(['POST'])
def resend_email_otp(request):
    email = request.data.get('email')
    try:
        otp_device = devices_for_user(EmailOtp, email=email).get()
    except ObjectDoesNotExist:
        return JsonResponse({'message': 'No OTP found'}, status=400)

    otp_device.generate_challenge()
    otp_device.save()

    sns = boto3.client('sns', region_name=settings.AWS_SNS_REGION)
    sns.publish(
        TopicArn=settings.AWS_SNS_TOPIC_ARN,
        Message=f'Your OTP is: {otp_device.token()}',
    )

    return Response({'message': 'OTP resent successfully'})
