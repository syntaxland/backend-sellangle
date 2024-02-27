from django.contrib import admin
from . import models


@admin.register(models.MarketPlaceSellerAccount)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        'created_at',
        'seller',
        'rating',
        'business_name',
        'business_reg_num',
        'business_address',
        'business_phone',
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
        'ad_save_count',
        'ad_view_count',
        # 'description',
        'is_active',
        'image1',
        'duration',
        'is_ad_reported',
        'ad_report_count',
        'ad_report',
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
        'ad_charges',
        # 'ad_charge_hours',
        'country',
        'state_province',
        'city',
        'condition',
        'currency',
        'price',
        'promo_code',
        'discount_percentage',
        'show_strike_through_promo_price',
        'ad_save_count',
        'ad_view_count',
        # 'description',
        'is_active',
        'is_ad_reported',
        'ad_report_count',
        'ad_report',
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

@admin.register(models.FreeAdMessageId)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'free_ad_message_id',
        'message',
        'free_ad',
        'timestamp',
    )  

@admin.register(models.PaidAdMessageId)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'paid_ad_message_id',
        'message',
        'paid_ad',
        'timestamp',
    )  


@admin.register(models.Message)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        'timestamp',
        'user',
        'message',
        'free_ad_message_id',
        'paid_ad_message_id',
        'buyer_free_ad_msg_count',
        'buyer_paid_ad_msg_count',
        'seller_free_ad_msg_count',
        'seller_paid_ad_msg_count',
        'free_ad',
        'paid_ad',

    )  

@admin.register(models.ReportFreeAd)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        'timestamp',
        'user',
        'free_ad',
        'ad_report',
    )  


@admin.register(models.ReportPaidAd)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        'timestamp',
        'user',
        'paid_ad',
        'ad_report',
    )  


@admin.register(models.ReviewFreeAdSeller)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        'timestamp',
        'seller',
        # 'seller_account',
        'user',
        'free_ad',
        'rating',
        'review_count',
        'is_review_liked',
        'review_like_count',
        'comment',
    )  


@admin.register(models.ReviewPaidAdSeller)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        'timestamp',
        'seller',
        # 'seller_account',
        'user',
        'paid_ad',
        'rating',
        'review_count',
        'is_review_liked',
        'review_like_count',
        'comment',
    )  


@admin.register(models.AdChargeTotal)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        'seller',
        'paid_ad',
       'total_ad_charges',
        'total_ad_charge_hours',
        'total_ad_charge_id',
        'timestamp',
    )  
