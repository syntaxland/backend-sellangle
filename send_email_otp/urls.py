from django.urls import path
from . import views, send_email_otp_sendinblue, send_email_otp_aws_ses
# from . import send_email_otp_sns
# from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    # using aws ses
    path('send-email-otp/', send_email_otp_sendinblue.send_email_otp, name='send_email_otp'),
    path('resend-email-otp/', send_email_otp_sendinblue.resend_email_otp, name='resend_email_otp'),
    path('verify-email-otp/', views.verify_email_otp, name='verify_email_otp'),
    # using aws ses
    # path('send_email_otp/', send_email_otp_aws_ses.send_email_otp, name='send_email_otp'),
    # path('resend_email_otp/', send_email_otp_aws_ses.resend_email_otp, name='resend_email_otp'),
]
