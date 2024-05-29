# promo/views.py
import random
import string

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# from app.models import OrderItem, Order, Product
from .models import PromoCode, Referral
from .serializers import PromoCodeSerializer, ReferralSerializer
# from app.serializer import ProductSerializer 
from decimal import Decimal, ROUND_DOWN
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from django.utils import timezone

from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_promo_code(request):
    data = request.data
    serializer = PromoCodeSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def generate_referral_code():
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choices(letters_and_digits, k=9)) 


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def generate_referral_link(request):
    user = request.user
    url = settings.SELLANGLE_URL 
    print("url:", url)
    try:
        if not user.referral_code:
            user.referral_code = generate_referral_code()
            user.save()
        if not user.referral_link:
            # referral_link =  f"http://localhost:3000/register?ref={user.referral_code}"
            # referral_link =  f"http://mcdofglobal.s3-website-us-east-1.amazonaws.com/register?ref={user.referral_code}"
            referral_link =  f"{url}/register?ref={user.referral_code}"
            user.referral_link = referral_link
            user.save()
        return Response(
            {
                "message": "Referral link and code generated successfully.",
                "referral_link": user.referral_link,
                "referral_code": user.referral_code,
            },
            status=status.HTTP_201_CREATED,
        )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def generate_referral_link_button(request):
    user = request.user
    try:
        if user.referral_code:
            user.referral_code = generate_referral_code()
            user.save()
        if user.referral_link:
            referral_link =  f"http://localhost:3000/register?ref={user.referral_code}"
            # referral_link =  f"http://mcdofglobal.s3-website-us-east-1.amazonaws.com/register?ref={user.referral_code}"
            user.referral_link = referral_link
            user.save()
        return Response(
            {
                "message": "Referral link and code generated successfully.",
                "referral_link": user.referral_link,
                "referral_code": user.referral_code,
            },
            status=status.HTTP_201_CREATED,
        )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_referrals(request):
    user = request.user
    try:
        referrals = Referral.objects.filter(referrer=user).order_by('-created_at')
        serializer = ReferralSerializer(referrals, many=True)
        return Response(serializer.data)
    except Referral.DoesNotExist:
        return Response({'detail': 'User referrals not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
# @permission_classes([IsAdminUser])
@permission_classes([IsAuthenticated])
def get_all_referrals(request):
    try:
        referrals = Referral.objects.all().order_by('-created_at')
        serializer = ReferralSerializer(referrals, many=True)
        return Response(serializer.data)
    except Referral.DoesNotExist:
        return Response({'detail': 'Referrals not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def refer_user(request):
    referral_code = request.data.get("referral_code")
    referred_by = request.user
    try:
        referral = Referral.objects.get(referral_code=referral_code)
        referral.referred_by = referred_by
        referral.save()
        return Response({"message": "User referred successfully"})
    except Referral.DoesNotExist:
        return Response({"error": "Referral code not found"}, status=400)


