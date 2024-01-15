# support/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

ROOM_TOPIC = (
        ('support', 'Support'),
        ('billing', 'Billing'),
        ('abuse', 'Abuse'), 
        ('otp', 'OTP'),
        ('payments', 'Payments'),
        ('transactions', 'Transactions'), 
        ('payouts', 'Payouts'),
        ('services', 'Services'),
        ('credit_points', 'Credit Points'),
        ('account_funds', 'Account Funds'),
        ('referrals', 'Referrals'),
        ('others', 'Others'),
    )


class SupportTicket(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="support_ticket_user")
    subject = models.CharField(max_length=225, null=True, blank=True)
    category = models.CharField(max_length=225, null=True, blank=True, choices=ROOM_TOPIC)
    ticket_id = models.CharField(max_length=12, unique=True, null=True)
    message = models.TextField(max_length=5000, null=True, blank=True,)
    is_closed = models.BooleanField(default=False)  
    is_resolved = models.BooleanField(default=False)  
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.user} {self.ticket_id}" 


class SupportResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="support_response_user")
    support_ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name='support_response', blank=True, null=True)
    message = models.TextField(max_length=5000, null=True, blank=True,)
    rating = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True) 
    modified = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return f"{self.support_ticket}"
