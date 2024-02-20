# marketplace/serializers.py
from rest_framework import serializers
from .models import (MarketPlaceSellerAccount, MarketplaceSellerPhoto, 
                     PostFreeAd, PostPaidAd, PaysofterApiKey, Message,
                     ReportFreeAd, ReportPaidAd, ReviewFreeAdSeller, ReviewPaidAdSeller,
                     FreeAdMessageId, PaidAdMessageId, AdChargeTotal
                     )


class MarketPlaceSellerAccountSerializer(serializers.ModelSerializer):
    business_phone = serializers.CharField(source='seller.phone_number', read_only=True)
    seller_phone = serializers.CharField(source='seller.phone_number', read_only=True)
    seller_username = serializers.CharField(source='seller.username', read_only=True)
    seller_joined_since = serializers.CharField(source='seller.created_at', read_only=True)

    class Meta:
        model = MarketPlaceSellerAccount
        fields = '__all__'
        extra_kwargs = {'id_card_image': {'required': True}}


class MarketplaceSellerPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketplaceSellerPhoto
        fields = '__all__'
        extra_kwargs = {'photo': {'required': True}}


class PostFreeAdSerializer(serializers.ModelSerializer):
    seller_avatar_url = serializers.SerializerMethodField()

    seller_phone = serializers.CharField(source='seller.phone_number', read_only=True)
    seller_username = serializers.CharField(source='seller.username', read_only=True)
    seller_joined_since = serializers.CharField(source='seller.created_at', read_only=True)
    class Meta:
        model = PostFreeAd
        fields = '__all__'
        extra_kwargs = {'image1': {'required': True}, 'image2': {'required': True}, 'image3': {'required': True}}

    def get_seller_avatar_url(self, obj):
        request = self.context.get('request')
        return request and request.get('seller_avatar_url', None)

class PostPaidAdSerializer(serializers.ModelSerializer):
    seller_avatar_url = serializers.SerializerMethodField()

    seller_phone = serializers.CharField(source='seller.phone_number', read_only=True)
    seller_username = serializers.CharField(source='seller.username', read_only=True)
    seller_joined_since = serializers.CharField(source='seller.created_at', read_only=True)

    class Meta:
        model = PostPaidAd
        fields = '__all__'
        extra_kwargs = {'image1': {'required': True}, 'image2': {'required': True}, 'image3': {'required': True}}

    def get_seller_avatar_url(self, obj):
        request = self.context.get('request')
        return request and request.get('seller_avatar_url', None)


class PaysofterApiKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaysofterApiKey
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    free_ad_buyer = serializers.CharField(source='user.username', read_only=True)
    free_ad_id = serializers.CharField(source='free_ad.id', read_only=True)
    free_ad_name = serializers.CharField(source='free_ad.ad_name', read_only=True)
    free_ad_price = serializers.CharField(source='free_ad.price', read_only=True)
    free_ad_currency = serializers.CharField(source='free_ad.currency', read_only=True)
    free_ad_expiration_date = serializers.CharField(source='free_ad.expiration_date', read_only=True)
    free_ad_rating = serializers.CharField(source='free_ad.ad_rating', read_only=True)
    free_ad_image1 = serializers.CharField(source='free_ad.image1.photo.url', read_only=True)
    free_seller_username = serializers.CharField(source='free_ad.seller.username', read_only=True)
    free_ad_message_id = serializers.CharField(source='free_ad_message_id.free_ad_message_id', read_only=True)
    
    sellerAvatarUrl = serializers.CharField(source='free_ad.seller.photo.url', read_only=True)

    paid_ad_id = serializers.CharField(source='paid_ad.id', read_only=True)
    paid_ad_name = serializers.CharField(source='paid_ad.ad_name', read_only=True)
    paid_ad_id = serializers.CharField(source='paid_ad.id', read_only=True)
    paid_ad_name = serializers.CharField(source='paid_ad.ad_name', read_only=True)
    paid_ad_price = serializers.CharField(source='paid_ad.price', read_only=True)
    paid_ad_currency = serializers.CharField(source='paid_ad.currency', read_only=True)
    paid_ad_expiration_date = serializers.CharField(source='paid_ad.expiration_date', read_only=True)
    paid_ad_rating = serializers.CharField(source='paid_ad.ad_rating', read_only=True)
    paid_ad_image1 = serializers.CharField(source='paid_ad.image1.photo.url', read_only=True)
    paid_seller_username = serializers.CharField(source='paid_ad.seller.username', read_only=True)
    free_ad_messagpaid_ad_message_ide_id = serializers.CharField(source='paid_ad_message_id.paid_ad_message_id', read_only=True)

    class Meta:
        model = Message
        fields = '__all__'
        extra_kwargs = {'image1': {'required': True}, 'image2': {'required': True}, 'image3': {'required': True}}


class ReportFreeAdSerializer(serializers.ModelSerializer):
    seller_username = serializers.CharField(source='seller.username', read_only=True)
    class Meta:
        model = ReportFreeAd
        fields = '__all__'


class ReportPaidAdSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    class Meta:
        model = ReportPaidAd
        fields = '__all__'


class ReviewFreeAdSellerSerializer(serializers.ModelSerializer):
    seller_username = serializers.CharField(source='seller.username', read_only=True)
    buyer_username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = ReviewFreeAdSeller
        fields = '__all__'


class ReviewPaidAdSellerSerializer(serializers.ModelSerializer):
    seller_username = serializers.CharField(source='seller.username', read_only=True)
    buyer_username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = ReviewPaidAdSeller
        fields = '__all__'


class FreeAdMessageIdSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    free_ad_buyer = serializers.CharField(source='user.username', read_only=True)
    free_ad_id = serializers.CharField(source='free_ad.id', read_only=True)
    free_ad_name = serializers.CharField(source='free_ad.ad_name', read_only=True)
    free_ad_price = serializers.CharField(source='free_ad.price', read_only=True)
    free_ad_currency = serializers.CharField(source='free_ad.currency', read_only=True)
    free_ad_expiration_date = serializers.CharField(source='free_ad.expiration_date', read_only=True)
    free_ad_rating = serializers.CharField(source='free_ad.ad_rating', read_only=True)
    free_ad_image1 = serializers.CharField(source='free_ad.image1.photo.url', read_only=True)
    free_seller_username = serializers.CharField(source='free_ad.seller.username', read_only=True)
    class Meta:
        model = FreeAdMessageId
        fields = '__all__'


class PaidAdMessageIdSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = PaidAdMessageId
        fields = '__all__'


class AdChargeTotalSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='seller.username', read_only=True)
    class Meta:
        model = AdChargeTotal
        fields = '__all__'
