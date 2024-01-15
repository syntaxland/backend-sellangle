from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class SendMessageInbox(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField(max_length=5000, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
