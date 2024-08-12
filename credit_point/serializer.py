# credit_point/serializers.py
from rest_framework import serializers
from .models import (CreditPoint,
                    BuyCreditPoint,
                    BuyUsdCreditPoint,
                    SellCreditPoint,
                    AdChargeCreditPoint,
                    CpsBonus,
                    SellCpsToSellangle, 

                     )
 
from django.contrib.auth import get_user_model

User = get_user_model() 



class CreditPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditPoint
        fields = "__all__"


class BuyCreditPointSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = BuyCreditPoint
        fields = '__all__'


class BuyUsdCreditPointSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = BuyUsdCreditPoint
        fields = '__all__'


class SellCreditPointSerializer(serializers.ModelSerializer):
    seller_username = serializers.CharField(source='seller.username', read_only=True)
    buyer_username = serializers.CharField(source='buyer.username', read_only=True)
    class Meta:
        model = SellCreditPoint
        fields = "__all__" 


class SellCpsToSellangleSerializer(serializers.ModelSerializer):
    seller_username = serializers.CharField(source='seller.username', read_only=True)
    buyer_username = serializers.CharField(source='buyer.username', read_only=True)
    class Meta:
        model = SellCpsToSellangle
        fields = "__all__" 


class AdChargeCreditPointSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = AdChargeCreditPoint
        fields = "__all__" 


class CpsBonusSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = CpsBonus
        fields = '__all__'
