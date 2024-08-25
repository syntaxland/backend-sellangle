# credit_point/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model() 

BUY_CPS_CHOICES = (
    ('500', '500 cps for NGN 500'),
    ('1000', '1,000 cps for NGN 1,000'),
    ('5000', '5,200 cps for NGN 5,000'),
    ('10000', '10,800 cps for NGN 10,000'),
    ('15000', '16,500 cps for NGN 15,000'),
    ('20000', '24,000 cps for NGN 20,000'),
    ('60000', '60,000 cps for NGN 50,000'),
    ('100000', '125,000 cps for NGN 100,000'),
    ('200000', '255,000 cps for NGN 200,000'),
    ('500000', '700,000 cps for NGN 500,000'),
    ('1000000', '1,500,000 cps for NGN 1,000,000'),
)

USD_CPS_CHOICES = (
    ('1', '1,000 cps for USD 1'),
    ('5', '5,200 cps for USD 5'),
    ('10', '10,800 cps for USD 10'),
    ('15', '16,500 cps for USD 15'),
    ('20', '24,000 cps for USD 20'),
    ('60', '60,000 cps for USD 50'),
    ('100', '125,000 cps for USD 100'),
    ('200', '255,000 cps for USD 200'),
    ('500', '700,000 cps for USD 500'),
    ('1000', '1,500,000 cps for USD 1,000'),
)

CPS_BONUS_TYPE_CHOICES = (
    ('Referral Bonus', 'Referral Bonus'),
    ('Sign-up Bonus', 'Sign-up Bonus'),
    ('Birthday Bonus', 'Birthday Bonus'),
    ('Loyalty Bonus', 'Loyalty Bonus'),
    ('Earned Bonus', 'Earned Bonus'),
    ('Other Bonus', 'Other Bonus'),
)


CURRENCY_CHOICES = (
        ('NGN', 'Nigerian Naira'),
        ('USD', 'United States Dollar'),
        ('GBP', 'British Pound Sterling'),
        ('EUR', 'Euro'),  
        ('JPY', 'Japanese Yen'),
        ('CAD', 'Canadian Dollar'),
        ('AUD', 'Australian Dollar'),
        ('INR', 'Indian Rupee'),
        ('CNY', 'Chinese Yuan'),
        ('ZAR', 'South African Rand'),
        ('BRL', 'Brazilian Real'),
        ('KES', 'Kenyan Shilling'),
        ('GHS', 'Ghanaian Cedi'),
        ('AED', 'United Arab Emirates Dirham'),
        ('SAR', 'Saudi Riyal'),
        ('GBP', 'British Pound Sterling'),
    )


class CreditPoint(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

  
class BuyCreditPoint(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='buy_credit_point_user')
    amount = models.CharField(max_length=100, null=True, blank=True, editable=False)
    cps_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    cps_purchase_id = models.CharField(max_length=50, unique=True)
    old_bal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    new_bal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_success = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True) 
     

class SellCreditPoint(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='buyer_credit_point')
    seller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='seller_credit_point')
    amount = models.DecimalField(max_digits=50, decimal_places=2, default=0, editable=False)
    cps_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    cps_sell_id = models.CharField(max_length=50, unique=True, blank=True)
    buyer_old_bal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    buyer_new_bal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    seller_old_bal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    seller_new_bal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_success = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True) 


class SellCpsToSellangle(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sell_cps_to_sellangle_buyer')
    seller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='ssell_cps_to_sellangle_seller')
    cps_sold_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="cps_sold_by_user")
    amount = models.DecimalField(max_digits=50, decimal_places=2, default=0, editable=False)
    cps_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, null=True, blank=True)
    paysofter_account_id = models.CharField(max_length=50, blank=True)
    paysofter_seller_id = models.CharField(max_length=50, blank=True)
    cps_checkout_link = models.CharField(max_length=225, null=True, blank=True)
    cps_sell_id = models.CharField(max_length=50, unique=True, blank=True)
    buyer_old_bal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    buyer_new_bal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    seller_old_bal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    seller_new_bal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_success = models.BooleanField(default=False)
    is_fulfilled = models.BooleanField(default=False)
    paysofter_promise_id = models.CharField(max_length=50, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True) 


class BuyUsdCreditPoint(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='usd_cps_user')
    amount = models.CharField(max_length=100, null=True, blank=True, editable=False)
    cps_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    usd_cps_purchase_id = models.CharField(max_length=50, unique=True, blank=True)
    old_bal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    new_bal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_success = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class AdChargeCreditPoint(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='ad_charge_credit_point_user')
    cps_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    ad_charge_cps_id = models.CharField(max_length=50, unique=True) 
    old_bal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    new_bal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_success = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True) 


class CpsBonus(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='cps_bonus_user')
    cps_bonus_type = models.CharField(max_length=100, choices=CPS_BONUS_TYPE_CHOICES, null=True, blank=True, editable=False)
    cps_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    cps_bonus_id = models.CharField(max_length=50, unique=True, blank=True)
    old_bal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    new_bal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_success = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
