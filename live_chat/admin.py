# live_chat/admin.py
from django.contrib import admin
from . import models


@admin.register(models.ChatRoom)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('room_name', 'id', 'created_at', )  
    search_fields = ('room_name',)

    # def get_readonly_fields(self, request, obj=None):
    #     readonly_fields = ['room_name', ]
    #     if obj and obj.is_superuser:
    #         readonly_fields.remove('name', )
    #     return readonly_fields


@admin.register(models.ChatMessage)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('room', 'user', 'message', 'timestamp',  )  
    search_fields = ('name',)

    # def get_readonly_fields(self, request, obj=None):
    #     readonly_fields = ['room', 'user', 'message', ]
    #     if obj and obj.is_superuser:
    #         readonly_fields.remove('content', )
    #     return readonly_fields
