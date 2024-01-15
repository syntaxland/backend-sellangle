# app/serializers.py
from django.db import models
from rest_framework import serializers
# from django.contrib.auth.models import User
from app.models import Product
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Product, Review, Order, OrderItem, ShippingAddress, Review
from user_profile.serializers import UserSerializer
from promo.serializers import PromoCodeSerializer


from django.contrib.auth import get_user_model

User = get_user_model()  

class ProductSerializer(serializers.ModelSerializer):
    promo_code = serializers.CharField(source='promo_code.promo_code', read_only=True)
    expiration_date = serializers.CharField(source='promo_code.expiration_date', read_only=True)
    discount_percentage = serializers.CharField(source='promo_code.discount_percentage', read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
        

class OrderSerializer(serializers.ModelSerializer): 
    user = UserSerializer()

    class Meta:
        model = Order
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    order = OrderSerializer()
    order_id = serializers.CharField(source='order.order_id', read_only=True)
    # isPaid = serializers.CharField(source='order.isPaid', read_only=True)
    email = serializers.CharField(source='order.user.email', read_only=True)
    first_name = serializers.CharField(source='order.user.first_name', read_only=True)

    class Meta:
        model = OrderItem
        fields = '__all__'


class ShippingAddressSerializer(serializers.ModelSerializer):
    order = OrderSerializer()
    order_id = serializers.CharField(source='order.order_id', read_only=True)
    email = serializers.CharField(source='order.user.email', read_only=True)
    first_name = serializers.CharField(source='order.user.first_name', read_only=True)

    class Meta:
        model = ShippingAddress
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    order = OrderSerializer()
    user = UserSerializer()
    product = ProductSerializer()
    order_item = OrderItemSerializer()
    order_id = serializers.CharField(source='order_item.order.order_id', read_only=True)
    # email = serializers.CharField(source='order_item.user.email', read_only=True)
    # product = serializers.CharField(source='order_item.product.name', read_only=True)
    # first_name = serializers.CharField(source='order_item.user.first_name', read_only=True)

    class Meta:
        model = Review
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', '_id', 'username', 'email', 'name', 'isAdmin']

    def get_name(self, obj):
        name = obj.first_name
        if name == "":
            name = obj.email
        return name

    def get__id(self, obj):
        return obj.id

    def get_isAdmin(self, obj):
        return obj.is_staff


# class UserSerializerWithToken(UserSerializer):
#     token = serializers.SerializerMethodField(read_only=True)

#     class Meta:
#         model = User
#         fields = ['id', '_id', 'username', 'email', 'name', 'isAdmin', 'token']

#     def get_token(self, obj):
#         token = RefreshToken.for_user(obj)
#         return str(token.access_token)
