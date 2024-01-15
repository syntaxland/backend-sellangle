from django.contrib import admin
from .models import EmailOtp


class EmailOtpAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'email_otp', 'created_at', 'expired_at')

admin.site.register(EmailOtp, EmailOtpAdmin)

