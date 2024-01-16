# credit_point/models.py
from django.db import models
from app.models import Order
from payment.models import Payment
# from promo.models import Referral
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


class CreditPoint(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)


class CreditPointEarning(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='credit_point_earning_user')
    order_payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True, related_name='credit_point_earnings')
    credit_points_earned = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)


class CreditPointRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, related_name='credit_point_user')
    order_payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True, related_name='credit_point_order')
    account_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=10)
    bank_name = models.CharField(max_length=100)
    credit_point_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, editable=False)
    request_ref = models.CharField(max_length=10, unique=True, blank=True)
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    is_delivered = models.BooleanField(default=False)
    delivered_at = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
 

class CreditPointPayment(models.Model):
    order_payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True, related_name='credit_point_order_payment')
    referrer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="referrer_credit_point_payment")
    credit_points_earned = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    referral_credit_points_bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.referrer.username if self.referrer else 'No Referrer'

  
class BuyCreditPoint(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='buy_credit_point_user')
    amount = models.CharField(max_length=100, choices=BUY_CPS_CHOICES, null=True, blank=True, editable=False)
    cps_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    cps_purchase_id = models.CharField(max_length=10, unique=True)
    is_success = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True) 
     

class SellCreditPoint(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='buyer_credit_point')
    seller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='seller_credit_point')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    cps_sell_id = models.CharField(max_length=10, unique=True, blank=True)
    is_success = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class BuyUsdCreditPoint(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='usd_cps_user')
    amount = models.CharField(max_length=100, choices=USD_CPS_CHOICES, null=True, blank=True, editable=False)
    cps_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    usd_cps_purchase_id = models.CharField(max_length=10, unique=True, blank=True)
    is_success = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

