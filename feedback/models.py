# feedback/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

ROOM_TOPIC = (
        ('Support', 'Support'),
        ('Billing', 'Billing'),
        ('Abuse', 'Abuse'), 
        ('OTP', 'OTP'),
        ('Payments', 'Payments'),
        ('Transactions', 'Transactions'), 
        ('Payouts', 'Payouts'),
        ('Services', 'Services'),
        ('Credit Points', 'Credit Points'),
        ('Account Funds', 'Account Funds'),
        ('Referrals', 'Referrals'),
        ('Others', 'Others'),
    )

 
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="feedback_user")
    category = models.CharField(max_length=225, null=True, blank=True, choices=ROOM_TOPIC)
    subject = models.CharField(max_length=225, null=True, blank=True)
    message = models.TextField(max_length=5000, null=True, blank=True,)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return f"{self.subject}"



