from django.contrib import admin
from . import models


@admin.register(models.User)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'created_at', 'id', 'first_name',  
                    'phone_number',  'is_verified','referral_code', 'referral_link',
                      'is_marketplace_seller', 'is_ecommerce_seller', 
                      'is_staff', 'is_superuser', 
                      )

    # # Add custom methods to display 'email', 'first_name', 'last_name'
    # def username(self, obj):
    #     return obj.user.username 

    
    # def email(self, obj):
    #     return obj.user.email

    # def first_name(self, obj):
    #     return obj.user.first_name

    # def last_name(self, obj):
    #     return obj.user.last_name

    # # Optional: This is used to set the column headers for 'email', 'first_name', and 'last_name'
    # email.short_description = 'Email'
    # first_name.short_description = 'First Name'
    # last_name.short_description = 'Last Name'
