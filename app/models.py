# app/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model() 

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='./images/products', null=True, blank=True)
    brand = models.CharField(max_length=200, null=True, blank=True)
    category = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    rating = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, editable=False)
    numReviews = models.IntegerField(null=True, blank=True, default=0, editable=False)
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    promo_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    promo_code = models.ForeignKey('promo.PromoCode', on_delete=models.SET_NULL, null=True, blank=True)
    countInStock = models.IntegerField(null=True, blank=True, default=0)
    save_count = models.PositiveIntegerField(default=0, editable=False)
    view_count = models.PositiveIntegerField(default=0, editable=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return self.name

    def get_discount_percentage(self):
        if self.promo_price:
            return ((self.price - self.promo_price) / self.price) * 100
        return 0


class Order(models.Model):
    order_id = models.CharField(max_length=10, unique=True, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    paymentMethod = models.CharField(max_length=200, null=True, blank=True)
    taxPrice = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    shippingPrice = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    promo_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    totalPrice = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    promo_total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    isPaid = models.BooleanField(default=False)
    paidAt = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    isDelivered = models.BooleanField(default=False)
    deliveredAt = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    _id = models.AutoField(primary_key=True, editable=False)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return F"{self.order_id} - {str(self.user)} - {str(self.createdAt)}" 


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, related_name='orderItems')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    qty = models.IntegerField(null=True, blank=True, default=0)
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True) 
    image = models.CharField(max_length=200, null=True, blank=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return self.name


class ShippingAddress(models.Model):
    order = models.OneToOneField(Order, on_delete=models.SET_NULL, null=True, blank=True, related_name='shippingAddress')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    isDelivered = models.BooleanField(default=False)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    postalCode = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    shippingPrice = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True) 
    _id = models.AutoField(primary_key=True, editable=False)
 
    def __str__(self):
        return self.address

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.OneToOneField(Order, on_delete=models.SET_NULL, null=True, blank=True, related_name='order_review')
    order_item = models.OneToOneField(OrderItem, on_delete=models.SET_NULL, null=True, blank=True, related_name='order_item_review')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) 
    name = models.CharField(max_length=200, null=True, blank=True)
    rating = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    _id = models.AutoField(primary_key=True, editable=False)
    createdAt = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.rating)
 