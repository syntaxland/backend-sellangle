from django.contrib import admin
from . import models


@admin.register(models.SendEmailMessage)
class AuthorAdmin(admin.ModelAdmin):
    
    list_display = (
        'subject',
        'sender_user',
        'receiver_user',
        'message',
        'timestamp',) 
    
    search_fields = (
        'sender_user',
        'receiver_user',
        'subject',
        'message',)
