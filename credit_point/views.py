# credit_point/views.py
from decimal import Decimal
import random
import string

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView 

from .serializer import (CreditPointSerializer, CreditPointRequestSerializer, 
                         CreditPointPaymentSerializer, CreditPointEarningSerializer,
                           BuyCreditPointSerializer, SellCreditPointSerializer)
from .models import (CreditPoint,  CreditPointRequest,
                      CreditPointPayment, CreditPointEarning, 
                      BuyCreditPoint, SellCreditPoint)
from django.db import transaction
from django.contrib.auth import get_user_model

User = get_user_model() 


def generate_credit_point_request_ref():
    letters_and_digits = string.ascii_uppercase + string.digits
    return 'CPR'+''.join(random.choices(letters_and_digits, k=7))

def generate_cps_purchase_id():
    letters_and_digits = string.ascii_uppercase + string.digits
    return 'CPS'+''.join(random.choices(letters_and_digits, k=7))

def generate_cps_sell_id():
    letters_and_digits = string.ascii_uppercase + string.digits
    return 'CPS'+''.join(random.choices(letters_and_digits, k=7))

@api_view(['POST'])
@permission_classes([IsAuthenticated])  
def credit_point_request_view(request):
    user = request.user
    data = request.data
    data['user'] = user.id 
    request_ref = generate_credit_point_request_ref()
    print('request_ref:', request_ref)

    try:
        credit_point_amount = request.data.get('credit_point_amount')
        print('credit_point_amount:', credit_point_amount)
        account_name = request.data.get('account_name')
        account_number = request.data.get('account_number')
        bank_name = request.data.get('bank_name')

        credit_point_request = CreditPointRequest.objects.create(
            user=user,
            credit_point_amount=credit_point_amount,
            account_name=account_name,
            account_number=account_number,
            bank_name=bank_name,
            request_ref=request_ref,
        ) 
        credit_point_request.save()

        credit_point, created = CreditPoint.objects.get_or_create(user=user)
        balance = credit_point.balance
        credit_point.balance = 0
        credit_point.save()
        return Response({'success': f'Credit point request submitted successfully. Withdrew NGN {balance}'}, 
                        status=status.HTTP_201_CREATED)
    except CreditPointRequest.DoesNotExist:
            return Response({'detail': 'Credit point request not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_credit_point_request_view(request):
    user = request.user
    try:
        credit_point = CreditPointRequest.objects.filter(user=user).order_by('-created_at')
        serializer = CreditPointRequestSerializer(credit_point, many=True)
        return Response(serializer.data)
    except CreditPointRequest.DoesNotExist:
        return Response({'detail': 'Credit point not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
# @permission_classes([IsAdminUser])
@permission_classes([IsAuthenticated])
def get_all_credit_points_request_view(request):
    try:
        all_credit_points = CreditPointRequest.objects.all().order_by('-created_at')
        serializer = CreditPointRequestSerializer(all_credit_points, many=True)
        return Response(serializer.data)
    except CreditPointRequest.DoesNotExist:
        return Response({'detail': 'Credit point not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_credit_points_balance_view(request):
    try:
        credit_point, created = CreditPoint.objects.get_or_create(user=request.user)
        serializer = CreditPointSerializer(credit_point)
        return Response(serializer.data)
    except CreditPointRequest.DoesNotExist:
        return Response({'detail': 'Credit point balance not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_credit_point_earnings(request):
    user = request.user
    try:
        # user_credit_point_earnings = CreditPointEarning.objects.filter(user=user).order_by('-created_at')
        user_credit_point_earnings = CreditPointEarning.objects.filter(user=user).order_by('-created_at').select_related('user', 'order_payment')
        # print('user_credit_point_earnings:', user_credit_point_earnings)
        serializer = CreditPointEarningSerializer(user_credit_point_earnings, many=True)
        # print('user_credit_point_earnings serializer:',serializer)
        return Response(serializer.data)
    except CreditPointEarning.DoesNotExist:
        return Response({'detail': 'Credit point earnings not found'}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_credit_point(request):
    user = request.user
    try:
        credit_point = CreditPointPayment.objects.filter(referrer=user).order_by('-created_at')
        serializer = CreditPointPaymentSerializer(credit_point, many=True)
        return Response(serializer.data)
    except CreditPointPayment.DoesNotExist:
        return Response({'detail': 'Credit point payments not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
# @permission_classes([IsAdminUser]) 
@permission_classes([IsAuthenticated])
def get_all_credit_point(request):
    try:
        all_credit_points_payments = CreditPointPayment.objects.all().order_by('-created_at')
        serializer = CreditPointPaymentSerializer(all_credit_points_payments, many=True)
        return Response(serializer.data)
    except CreditPointPayment.DoesNotExist:
        return Response({'detail': 'Credit point payments not found'}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])  
@transaction.atomic
def buy_credit_point(request):
    user = request.user
    data = request.data
    print('data:', data)

    cps_purchase_id = generate_cps_purchase_id()
    print('cps_purchase_id:', cps_purchase_id)
    amount = Decimal(data.get('amount'))
    print('amount:', amount)

    AMOUNT_TO_CPS_MAPPING = {
    '500': 500,
    '1000': 1000,
    '5000': 5200,
    '10000': 10800,
    '15000': 16500,
    '20000': 24000,
    '50000': 60000,
    '100000': 125000,
    '200000': 255000,
    '500000': 700000,
    '1000000': 1500000,
    }

    cps_amount = AMOUNT_TO_CPS_MAPPING.get(str(amount), 0)
    print('cps_amount:', cps_amount)

    try:
        credit_point, created = CreditPoint.objects.get_or_create(user=user)
        balance = credit_point.balance
        print('cps balance(before):', balance)

        credit_point.balance += amount
        credit_point.save()

        buy_credit_point = BuyCreditPoint.objects.create( 
            user=user,
            amount=amount,
            cps_purchase_id=cps_purchase_id,
            cps_amount=cps_amount,
        )

        buy_credit_point.is_success = True
        buy_credit_point.save()
        print('cps balance(after):', credit_point.balance)

        return Response({'detail': f'Credit point request successful.'}, 
                        status=status.HTTP_201_CREATED)
    except CreditPoint.DoesNotExist:
            return Response({'detail': 'Credit point not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])  
def sell_credit_point(request):
    seller = request.user
    data = request.data
    print('data:', data)

    cps_sell_id = generate_cps_sell_id()
    print('cps_sell_id:', cps_sell_id)

    amount = Decimal(data.get('amount'))
    buyer_username = data.get('username')
    password = data.get('password')

    if not seller.check_password(password):
        return Response({'detail': 'Invalid password.'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        buyer = User.objects.get(username=buyer_username)
    except User.DoesNotExist:
        return Response({'detail': f'CPS Buyer/Receiver with username "{buyer_username}" not found.'}, status=status.HTTP_404_NOT_FOUND)
    print('buyer:', buyer)

    try:
        sell_credit_point = SellCreditPoint.objects.create(
            buyer=buyer,
            seller=seller,
            amount=amount,
            cps_sell_id=cps_sell_id, 
        )

        seller_credit_point, created = CreditPoint.objects.get_or_create(user=seller)
        balance = seller_credit_point.balance
        if balance < amount: 
            return Response({'detail': 'Insufficient credit point balance. Fund your cps wallet and try again.'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        seller_credit_point.balance -= amount
        seller_credit_point.save()

        buyer_credit_point, created = CreditPoint.objects.get_or_create(user=buyer)
        balance = buyer_credit_point.balance
        buyer_credit_point.balance += amount
        buyer_credit_point.save()

        sell_credit_point.is_success = True
        sell_credit_point.save()

        return Response({'detail': f'Credit point request successful.'}, 
                        status=status.HTTP_201_CREATED)
    except CreditPoint.DoesNotExist:
            return Response({'detail': 'Credit point not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_buy_credit_point(request):
    user = request.user
    try:
        credit_point = BuyCreditPoint.objects.filter(user=user).order_by('-created_at')
        serializer = BuyCreditPointSerializer(credit_point, many=True) 
        return Response(serializer.data)
    except BuyCreditPoint.DoesNotExist:
        return Response({'detail': 'Credit point not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_seller_credit_point(request):
    user = request.user
    try:
        credit_point = SellCreditPoint.objects.filter(seller=user).order_by('-created_at')
        serializer = SellCreditPointSerializer(credit_point, many=True)
        return Response(serializer.data)
    except SellCreditPoint.DoesNotExist:
        return Response({'detail': 'Credit point not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_buyer_credit_point(request):
    user = request.user
    try:
        credit_point = SellCreditPoint.objects.filter(buyer=user).order_by('-created_at')
        serializer = SellCreditPointSerializer(credit_point, many=True)
        return Response(serializer.data)
    except SellCreditPoint.DoesNotExist:
        return Response({'detail': 'Credit point not found'}, status=status.HTTP_404_NOT_FOUND)
