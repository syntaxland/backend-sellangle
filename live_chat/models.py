# live_chat/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

ROOM_TOPIC = (
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

class ChatRoom(models.Model):
    room_name = models.CharField(max_length=255, unique=True)
    users = models.ManyToManyField(User, related_name='chat_rooms')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    room_topic = models.CharField(max_length=225, null=True, blank=True, choices=ROOM_TOPIC)
    
    def __str__(self):
        return self.room_name


class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages', null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='chat_message_user')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}: {self.message}'
 