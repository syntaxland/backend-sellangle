import random
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class EmailOtp(models.Model):
    email_otp = models.CharField(max_length=6)
    email = models.EmailField(max_length=100, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    expired_at = models.DateTimeField(null=True, blank=True)

    def is_valid(self):
        # return self.created_at >= timezone.now() - timezone.timedelta(minutes=30)
        return self.expired_at >= timezone.now()

    def generate_email_otp(self):
        self.email_otp = str(random.randint(100000, 999999))
        self.created_at = timezone.now()
        self.expired_at = timezone.now() + timezone.timedelta(minutes=30)
        self.save()

    class Meta:
        default_related_name = 'email_otp'
