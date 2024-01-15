from django.contrib import admin
from .models import PasswordResetToken


class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'token', 'created_at', 'expired_at')

admin.site.register(PasswordResetToken, PasswordResetTokenAdmin)
