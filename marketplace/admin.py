from django.contrib import admin
from . import models


@admin.register(models.MarketPlaceSellerAccount)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        'created_at',
        'seller',
        'business_name',
        'business_reg_num',
        'business_address',
        'business_status',
        'staff_size',
        'business_industry',
        'business_category',
        'country',
        'id_card_image',
        'dob',
        'is_seller_verified',
    )  


@admin.register(models.MarketplaceSellerPhoto)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        'seller',
        'photo',
        'created_at',
    )  


@admin.register(models.PostFreeAd)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        'timestamp',
        'seller',
        'ad_name',
        'ad_category',
        'ad_type',
        'country',
        'state_province',
        'city',
        'condition',
        'currency',
        'price',
        'brand',
        'description',
        'is_active',
        'image1',
        'duration',
        'duration_hours',
        'expiration_date',
    )  

@admin.register(models.PostPaidAd)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        'timestamp',
        'seller',
        'ad_name',
        'ad_category',
        'ad_type',
        'country',
        'state_province',
        'city',
        'condition',
        'currency',
        'price',
        'brand',
        'description',
        'is_active',
        'image1',
        'duration',
        'duration_hours',
        'expiration_date',
    )  


@admin.register(models.PaysofterApiKey)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        # 'created_at',
        'seller',
        'live_api_key',
    )  


@admin.register(models.Message)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        'timestamp',
        'user',
        'free_ad',
        'paid_ad',
        'message',
    )  
