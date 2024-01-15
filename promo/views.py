# promo/views.py
import random
import string

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from app.models import OrderItem, Order, Product
from .models import PromoCode, Referral
from .serializers import PromoCodeSerializer, ReferralSerializer
from app.serializer import ProductSerializer
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


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated]) 
def apply_promo_code(request):
    data = request.data
    promo_code = data.get('promoCode')
    order_id = data.get('order_id')
    print('promo_code, order_id:', promo_code, order_id)

    try:
        promo = PromoCode.objects.get(promo_code=promo_code)
        if not promo.is_valid():
            return Response({'detail': 'Promo code has expired.'}, status=status.HTTP_400_BAD_REQUEST)
    except PromoCode.DoesNotExist:
        return Response({'detail': 'Invalid promo code.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        order_items_with_promo = OrderItem.objects.filter(product__promo_code__promo_code=promo_code, order__user=request.user, order__order_id=order_id)
        if not order_items_with_promo:
            return Response({'detail': 'Promo code not for this product.'}, status=status.HTTP_404_NOT_FOUND)
    except OrderItem.DoesNotExist:
        return Response({'detail': 'Order item does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

    promo_discount = 0
    discount_percentage = 0

    for product in order_items_with_promo:
        if product.product and product.product.promo_code:
            # Calculate discount for each product
            discount_percentage = product.product.promo_code.discount_percentage
            product_price = product.price
            discount_amount = (discount_percentage / 100) * product_price
            promo_discount += discount_amount

    promo_discount = promo_discount.quantize(Decimal('0.00'), rounding=ROUND_DOWN)
    print('apply_promo_code promo_discount:', promo_discount, 'discount_percentage:', discount_percentage)

    # Return the promo discount
    return Response({'promoDiscount': promo_discount, 'discountPercentage': discount_percentage}, status=status.HTTP_200_OK)




# @api_view(['POST', 'GET'])
# @permission_classes([IsAuthenticated])
# def apply_promo_code(request):
#     data = request.data
#     promo_code = data.get('promoCode')
#     order_id = data.get('order_id')
#     # product_id = data.get('product_id')
#     print('promo_code, order_id:', promo_code, order_id)

#     try:
#         promo = PromoCode.objects.get(promo_code=promo_code)
#         if not promo.is_valid():
#             return Response({'detail': 'Promo code has expired.'}, status=status.HTTP_400_BAD_REQUEST)
#     except PromoCode.DoesNotExist:
#         return Response({'detail': 'Invalid promo code.'}, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         order_items_with_promo = OrderItem.objects.filter(product__promo_code__promo_code=promo_code, order__user=request.user)
#         if not order_items_with_promo:
#             return Response({'detail': 'Order item(s) has/have no promo code.'}, status=status.HTTP_400_BAD_REQUEST)
#     except OrderItem.DoesNotExist:
#         return Response({'detail': 'Order item does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

#     order_items_with_promo = OrderItem.objects.filter(product__promo_code__promo_code=promo_code, order__user=request.user)
#     promo_discount = 0
#     for product in order_items_with_promo:
#         # Calculate discount for each product
#         discount_percentage = product.promo_code.discount_percentage
#         product_price = product.price
#         discount_amount = (discount_percentage / 100) * product_price
#         promo_discount += discount_amount

#     promo_discount = promo_discount.quantize(Decimal('0.00'), rounding=ROUND_DOWN)
#     print('apply_promo_code promo_discount:', promo_discount, 'discount_percentage:', product.promo_code.discount_percentage)

#     # Return the promo discount
#     return Response({'promoDiscount': promo_discount, 'discountPercentage': discount_percentage}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_valid_promo_products(request):
    current_datetime = timezone.now()
    promo_products = Product.objects.filter(promo_code__expiration_date__gt=current_datetime) 
    serializer = ProductSerializer(promo_products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


def generate_referral_code():
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choices(letters_and_digits, k=9)) 


# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def generate_referral_link(request):
#     user = request.user

#     try:
#         # if not user.referral_code:
#         #     # Generate and set the referral code if it doesn't exist
#         #     user.referral_code = generate_referral_code()
#         #     user.save()
            
#         referred_by, created = Referral.objects.get_or_create(referrer=user)

#         if not referred_by.referral_code:
#             # Generate a new referral code if it doesn't exist
#             referred_by.referral_code = generate_referral_code()
#             referred_by.save()

#         if not user.referral_link:
#             # Generate the referral link with the user's referral code
#             referral_link =  f"http://localhost:3000/register?ref={user.referral_code}"
#             # referral_link =  f"http://mcdofglobal.s3-website-us-east-1.amazonaws.com/register?ref={user.referral_code}"

#             # Save the referral link to the user's profile
#             user.referral_link = referral_link
#             user.save()

#         return Response(
#             {
#                 "message": "Referral link and code generated successfully.",
#                 "referral_link": user.referral_link,
#                 "referral_code": user.referral_code,
#             },
#             status=status.HTTP_201_CREATED,
#         )

#     except Exception as e:
#         return Response(
#             {"error": str(e)},
#             status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#         )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def generate_referral_link(request):
    user = request.user
    url = settings.MCDOFSHOP_URL
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



    
# @api_view(["POST"])
# @permission_classes([IsAuthenticated])
# def apply_promo_code(request):
#     promo_code = request.data.get("promo_code")
#     try:
#         promo = PromoCode.objects.get(promo_code=promo_code, expiration_date__gte=timezone.now())
#         return Response({
#             "message": "Promo code applied successfully",
#             "discount_percentage": promo.discount_percentage,
#             "expiration_date": promo.expiration_date
#         })
#     except PromoCode.DoesNotExist:
#         return Response({"error": "Invalid promo code or expired"}, status=400)
    

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


