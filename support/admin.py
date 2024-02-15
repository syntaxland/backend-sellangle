# support/admin.py
from django.contrib import admin
from . import models


@admin.register(models.SupportTicket)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 
                    'ticket_id',
                    'category',
                    'is_closed',
                    'is_resolved', 
                     'created_at',
                     )  


@admin.register(models.SupportResponse) 
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'support_ticket',
        'message', 
        'created_at',
            )  
    