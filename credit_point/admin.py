from django.contrib import admin
from . import models


@admin.register(models.CreditPointRequest)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'user', 'account_name', 'account_number', 
                    'bank_name', 'credit_point_amount', 'request_ref', 'is_paid', 'paid_at',
                    'is_delivered', 'delivered_at',)
    search_fields = ('account_number', 'user')  


@admin.register(models.CreditPoint)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('created_at', 
                    'user', 
                    # 'credit_points_earned', 
                    'balance', )

@admin.register(models.CreditPointPayment)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('created_at', 
                    'referrer', 
                    'referral_credit_points_bonus',
                     'order_payment', )


@admin.register(models.CreditPointEarning)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('created_at',
                     'user', 
                    'credit_points_earned', 
                    'order_payment',                  
                      )
    

@admin.register(models.BuyCreditPoint)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('created_at', 
                    'user', 
                    'amount',
                     'cps_amount', 
                     'cps_purchase_id', 
                     'is_success', 
                     'old_bal', 
                    'new_bal',
                     )


@admin.register(models.BuyUsdCreditPoint)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('created_at', 
                    'user', 
                    'amount',
                     'cps_amount', 
                     'usd_cps_purchase_id', 
                     'is_success', 
                     'old_bal', 
                    'new_bal',
                     )                    


@admin.register(models.SellCreditPoint)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('created_at',
                     'seller', 
                     'buyer', 
                    'amount',                  
                    'cps_sell_id', 
                    'is_success', 
                    'buyer_old_bal', 
                    'buyer_new_bal', 
                    'seller_old_bal', 
                    'seller_new_bal',
                      )

@admin.register(models.AdChargeCreditPoint)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user',
                     'cps_amount', 
                     'ad_charge_cps_id', 
                    'old_bal',                  
                    'new_bal', 
                    'created_at', 
                    
                      )


@admin.register(models.CpsBonus)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('created_at', 
                    'user', 
                    'cps_bonus_type',
                     'cps_amount', 
                     'cps_bonus_id', 
                     'is_success', 
                     'old_bal', 
                    'new_bal',
                     )
