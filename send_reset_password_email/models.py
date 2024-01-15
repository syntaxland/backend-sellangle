from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model

User = get_user_model()

 
class PasswordResetToken(models.Model):
    # user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    email = models.EmailField(max_length=100, unique=True, null=True, blank=True)
    token = models.CharField(max_length=32, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    expired_at = models.DateTimeField(null=True, blank=True)

    def is_valid(self):
        # Check if the token is within the valid time range (30 minutes)
        # return self.created_at >= timezone.now() - timezone.timedelta(minutes=30)
        return self.expired_at >= timezone.now()

    def generate_token(self):
        self.token = get_random_string(length=32)
        self.created_at = timezone.now()
        self.expired_at = timezone.now() + timezone.timedelta(minutes=30)
        self.save()

    class Meta:
        default_related_name = 'password_reset_tokens'
