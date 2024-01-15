from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.views import APIView

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

from .models import PasswordResetToken
from user_profile.serializers import UserSerializer
from .serializers import PasswordResetRequestSerializer, ResetPasswordSerializer

from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def send_password_reset_link_view(request):
    data=request.data
    serializer = PasswordResetRequestSerializer(data=data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        # first_name = serializer.validated_data['first_name']
        try:
            user = User.objects.get(email=email) 
        except User.DoesNotExist:
            return Response({'detail': 'No profile matches the given query.'}, status=status.HTTP_404_NOT_FOUND)
        try:
            # Send Password Reset Link
            token, created = PasswordResetToken.objects.get_or_create(email=email)
            token.generate_token()
            # Email Sending API Config
            configuration = sib_api_v3_sdk.Configuration()
            configuration.api_key['api-key'] = settings.SENDINBLUE_API_KEY
            api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
            # Sending email
            subject = "Password Reset Request"
            print("\nSending Password Reset link...")
            first_name = user.first_name 
            # first_name = data['first_name'].title() if data.get('first_name') else 'User'
            # password_reset_url = request.build_absolute_uri(reverse('password_reset', kwargs={'token': token.token}))
            # password_reset_url = "http://localhost:3000/reset-password/" + token.token
            password_reset_url = " http://mcdofglobal.s3-website-us-east-1.amazonaws.com/reset-password/" + token.token
            html_content = f"""
            <!DOCTYPE html>
            <html>
                <head>
                    <title>Password Reset Request</title>
                </head>
                <body>
                    <p>Hello { first_name.title() },</p>
                    <p>You have requested to reset your password for your McdofGlobal account. 
                    Click the link below to reset your password:</p>
                    <p><a href="{ password_reset_url }" style="display: inline-block; 
                    background-color: #2196f3; color: #fff; padding: 10px 20px; 
                    text-decoration: none;">Reset Password</a></p>
                    <p>This link is valid for 30 minutes.</p>
                    <p>If you didn't initiate this password reset request, please ignore it.</p>
                    <p>Best regards,</p>
                    <p>McdofGlobal Team</p>
                </body>
            </html>
            """
            sender_name = settings.EMAIL_SENDER_NAME
            sender_email = settings.EMAIL_HOST_USER
            sender = {"name": sender_name, "email": sender_email}
            to = [{"email": email, "name": first_name}]
            send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
                to=to,
                html_content=html_content, 
                sender=sender,
                subject=subject
            )
            try:
                api_response = api_instance.send_transac_email(send_smtp_email)
                print('\nPassord request link sent:', password_reset_url)
            except ApiException as e:
                print(e)
            return Response({'detail': 'Passord request link sent successfully.'}, status=status.HTTP_200_OK)
        except PasswordResetToken.DoesNotExist:
            return Response({'detail': 'User not found. Please check the email and try again'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    def post(self, request, token):
        data = request.data
        serializer = ResetPasswordSerializer(data=data)
        if serializer.is_valid():
            new_password = serializer.validated_data['new_password']
            try:
                token_obj = PasswordResetToken.objects.get(token=token)
                if token_obj.is_valid():
                    user = User.objects.get(email=token_obj.email)
                    user.set_password(new_password)
                    user.save()
                    token_obj.delete()  # Remove the token after successful reset
                    return Response({'detail': 'Password reset successful'}, status=status.HTTP_200_OK)
                else:
                    return Response({'detail': 'Password reset link has expired'}, status=status.HTTP_400_BAD_REQUEST)
            except PasswordResetToken.DoesNotExist:
                return Response({'detail': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
