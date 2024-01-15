from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from .models import EmailOtp
from .serializers import EmailOTPSerializer
from user_profile.serializers import UserSerializer 

from django.conf import settings
from django.contrib.auth import get_user_model
# from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_email_otp(request):
    serializer = EmailOTPSerializer(data=request.data)
    if serializer.is_valid():
        otp = serializer.validated_data['otp']
        try:
            email_otp = EmailOtp.objects.get(email_otp=otp)
            if email_otp.is_valid():
                email_otp.delete()

                user_email = email_otp.email
                try:
                    user = User.objects.get(email=user_email)
                    if user.is_verified:
                        return Response({'detail': f'User with email: {user_email} already verified. Please login.'}, status=status.HTTP_200_OK)
                    else:
                        user.is_verified = True
                        user.save()
                        print('Email verified successfully.')
                        return Response({'detail': 'Email verified successfully!'}, status=status.HTTP_200_OK)
                except User.DoesNotExist:
                    return Response({'detail': 'User not found. Please register again.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'detail': 'Invalid or expired OTP. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)
        except EmailOtp.DoesNotExist:
            return Response({'detail': 'Invalid OTP. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    