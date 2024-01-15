# promo/admin.py
from django.contrib import admin
from . import models


@admin.register(models.Referral)
class AuthorAdmin(admin.ModelAdmin):
    # list_display = ('created_at', 'id', 'referrer',  'referral_code', )
    list_display = ('created_at', 'id', 'referrer',  )
    search_fields = ('referrer__email',)
    list_filter = ('created_at',)
    # readonly_fields = ('referred_users_list',)

    # def referred_users_list(self, obj):
    #     # This function returns a comma-separated list of referred users
    #     return ", ".join([str(user) for user in obj.referred_users.all()])

    # referred_users_list.short_description = 'Referred Users'


@admin.register(models.ReferralBonus)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('created_at',  'referrer', 'referral_credit_points_bonus',) 


@admin.register(models.PromoCode)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('promo_code', 'discount_percentage', 'created_at', 'expiration_date') 
