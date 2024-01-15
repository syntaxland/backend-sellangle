
from rest_framework import serializers
from .models import PromoCode, Referral
from user_profile.serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model() 

class PromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCode
        fields = "__all__"


class ReferralSerializer(serializers.ModelSerializer):
    # referrer = UserSerializer()
    # referrer_email = serializers.CharField(source='referrer.email', read_only=True)
    # referrer_first_name = serializers.CharField(source='referrer.first_name', read_only=True)
    # referrer_last_name = serializers.CharField(source='referrer.last_name', read_only=True)

    # referred_users = UserSerializer()
    # referred_email = serializers.CharField(source='referred_users.email', read_only=True)
    # referred_first_name = serializers.CharField(source='referred_users.first_name', read_only=True)
    # referred_last_name = serializers.CharField(source='referred_users.last_name', read_only=True)
    class Meta:
        model = Referral
        fields = "__all__"
