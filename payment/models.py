# payment/models.py
from django.db import models
from app.models import Order
from django.contrib.auth import get_user_model

User = get_user_model() 

 
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, related_name='order_payment') 
    amount = models.DecimalField(max_digits=16, decimal_places=2, editable=False)
    items_amount = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True, editable=False)
    final_items_amount = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True, editable=False)
    promo_code_discount_amount = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True, default=0, editable=False)
    promo_code_discount_percentage = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, editable=False)
    final_total_amount = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True, editable=False)
    reference = models.CharField(max_length=14, unique=True, blank=True, editable=False) 
    payment_provider = models.CharField(max_length=50, null=True, blank=True) 
    is_success = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - NGN {self.amount} - {self.order.order_id}"
