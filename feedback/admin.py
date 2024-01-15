# support/admin.py
from django.contrib import admin
from . import models


@admin.register(models.Feedback)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 
                    'subject',
                    'message',
                     'created_at',
                     )  
    search_fields = ('subject',)

    # def get_readonly_fields(self, request, obj=None):
    #     readonly_fields = ['ticket_id', ]
    #     if obj and obj.is_superuser:
    #         readonly_fields.remove('message', )
    #     return readonly_fields
