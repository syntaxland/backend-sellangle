from django.contrib import admin
from . import models


@admin.register(models.SendMessageInbox)
class AuthorAdmin(admin.ModelAdmin):
    
    list_display = (
        'subject',
        'sender',
        'receiver',
        'message',
        'is_read',
        'timestamp',) 
    
    search_fields = (
        'sender',
        'receiver',
        'subject',
        'message',)
