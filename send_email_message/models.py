from django.db import models
from app.models import Order
from payment.models import Payment
from django.contrib.auth import get_user_model

User = get_user_model()


class SendEmailMessage(models.Model):
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='email_sender')
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='email_receiver')
    subject = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField(max_length=5000, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
 