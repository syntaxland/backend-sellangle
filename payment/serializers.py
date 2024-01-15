from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Payment
from user_profile.serializers import UserSerializer
from app.serializer import OrderSerializer

class PaymentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    order = OrderSerializer()
    order_id = serializers.CharField(source='order.order_id', read_only=True)
    email = serializers.CharField(source='order.user.email', read_only=True)
    first_name = serializers.CharField(source='order.user.first_name', read_only=True)
    
    class Meta:
        model = Payment
        fields = "__all__" 


class ListPaymentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    order = OrderSerializer()
    order_id = serializers.CharField(source='order.order_id', read_only=True)
    email = serializers.CharField(source='order.user.email', read_only=True)
    first_name = serializers.CharField(source='order.user.first_name', read_only=True)
 
    class Meta:
        model = Payment
        fields = "__all__"


class UserPaymentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    order = OrderSerializer()
    order_id = serializers.CharField(source='order.order_id', read_only=True)
    email = serializers.CharField(source='order.user.email', read_only=True)
    first_name = serializers.CharField(source='order.user.first_name', read_only=True)
 
    class Meta:
        model = Payment
        # fields = "__all__"
        fields = ['user', 'order', 'amount', 'reference', 'created_at', 'email', 'first_name', 'order_id']
