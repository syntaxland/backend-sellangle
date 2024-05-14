import random
import string
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from credit_point.models import CreditPoint, CpsBonus 
from send_message_inbox.models import SendMessageInbox

from .models import EmailOtp
from .serializers import EmailOTPSerializer
from user_profile.serializers import UserSerializer 

from django.conf import settings
from django.contrib.auth import get_user_model
# from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

User = get_user_model()


def generate_cps_id(): 
    letters_and_digits = string.ascii_uppercase + string.digits
    return 'CPS'+''.join(random.choices(letters_and_digits, k=16))


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

                        # create signup bonus
                        credit_point, created = CreditPoint.objects.get_or_create(user=user)
                        credit_point_balance = credit_point.balance
                        print('credit_point_balance:', credit_point_balance)
                        cps_bonus_type = "Sign-Up Bonus"
                        cps_bonus_amt = 100

                        credit_point.balance += cps_bonus_amt
                        credit_point.save()

                        credit_point = CreditPoint.objects.get(user=user)
                        cps_new_bal = credit_point.balance
                        print('cps_new_bal:', cps_new_bal)

                        CpsBonus.objects.create(
                            user=user,
                            cps_bonus_type=cps_bonus_type,
                            cps_amount=cps_bonus_amt,
                            old_bal=credit_point_balance,
                            new_bal=cps_new_bal, 
                            cps_bonus_id=generate_cps_id(),
                            is_success=True,
                        )

                        # send bonus msg
                        send_cps_bonus_msg(user, credit_point_balance, cps_bonus_amt)

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

    
def send_cps_bonus_msg(user, credit_point_balance, cps_bonus_amt):
    
    formatted_outstanding_cps_amount = '{:,.2f}'.format(float(credit_point_balance))
    formatted_cps_bonus_amt = '{:,.2f}'.format(float(cps_bonus_amt))

    message_content = f"""
        <html>
        <head>
            <title>Sign-Up Bonus</title>
        </head>
        <body>
            <p>Dear {user.username},</p>
            <p>Your credit point wallet has been credited with <b>{formatted_cps_bonus_amt} CPS</b> sign-up bonus.</p>
            <p>Congratulations on your successful sign-up!</p>
            <p>Best regards,<br>The Support Team</p>
        </body>
        </html>
    """

    inbox_message = SendMessageInbox.objects.create(
        receiver=user,
        subject="Sign-Up Bonus",
        message=message_content,
        is_read=False,
    )

    inbox_message.msg_count += 1
    inbox_message.save()
    
    print(f"Notification sent to {user.username} about sign-up bonus.")
