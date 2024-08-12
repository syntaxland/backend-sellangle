# credit_point/views.py
from decimal import Decimal
import random
import string

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response 
from rest_framework import status, generics
from rest_framework.views import APIView  
 

from .models import (CreditPoint,  
                      BuyCreditPoint, BuyUsdCreditPoint, 
                      SellCreditPoint,
                      AdChargeCreditPoint, CpsBonus,
                      SellCpsToSellangle, 
                      )

from .serializer import (BuyUsdCreditPointSerializer, CreditPointSerializer, 
                           BuyCreditPointSerializer, SellCreditPointSerializer,
                           AdChargeCreditPointSerializer, CpsBonusSerializer,
                         SellCpsToSellangleSerializer,
                           )

from send_message_inbox.models import SendMessageInbox
from django.db import transaction
from django.contrib.auth import get_user_model

User = get_user_model() 

def generate_cps_purchase_id():
    letters_and_digits = string.ascii_uppercase + string.digits
    return 'CPS'+''.join(random.choices(letters_and_digits, k=17))

def generate_cps_sell_id():
    letters_and_digits = string.ascii_uppercase + string.digits
    return 'CPS'+''.join(random.choices(letters_and_digits, k=17))


def send_sell_cps_msg_alert_to_buyer(request, buyer, seller, old_bal, new_bal, cps_amount):
    message_content = f"""
        <html>
        <head>
            <title>CPS Transaction</title>
        </head>
        <body>
            <p>Dear {buyer.first_name},</p>
            <p>Your credit point wallet has been credited with <b>{cps_amount} CPS</b> sent by <b>{seller.username}</b>.</p>
            <p>Old Bal: <b>{old_bal} CPS</b></p>
            <p>New Bal: <b>{new_bal} CPS</b></p>
            <p>Best regards,</p>
            <p>Sellangle Team</p>
        </body>
        </html>
    """
    inbox_message = SendMessageInbox.objects.create(
        receiver=buyer,
        subject="CPS Transaction",
        message=message_content,
        is_read=False,
    )
    inbox_message.msg_count += 1
    inbox_message.save()
    print(f"Notification sent to {buyer.username} about CPS Transaction.")


def send_sell_cps_msg_alert_to_seller(request, buyer, seller, old_bal, new_bal, cps_amount):
    message_content = f"""
        <html>
        <head>
            <title>CPS Transaction</title>
        </head>
        <body>
            <p>Dear {seller.first_name},</p>
            <p>Your credit point wallet has been debited with <b>{cps_amount} CPS</b> sold to <b>{buyer.username}</b>.</p>
            <p>Old Bal: <b>{old_bal} CPS</b></p>
            <p>New Bal: <b>{new_bal} CPS</b></p>
            <p>Best regards,</p>
            <p>Sellangle Team</p>
        </body>
        </html>
    """
    inbox_message = SendMessageInbox.objects.create(
        receiver=seller,
        subject="CPS Transaction",
        message=message_content,
        is_read=False,
    )
    inbox_message.msg_count += 1
    inbox_message.save()
    print(f"Notification sent to {seller.username} about CPS Transaction.")


def send_buy_cps_msg_alert_to_buyer(request, user, amount, currency, old_bal, new_bal, cps_amount):
    message_content = f"""
        <html>
        <head>
            <title>CPS Transaction</title>
        </head>
        <body>
            <p>Dear {user.first_name},</p>
            <p>Your credit point wallet has been credited with <b>{cps_amount} CPS</b> purchased for <b>{amount} {currency}</b>.</p>
            <p>Old Bal: <b>{old_bal} CPS</b></p>
            <p>New Bal: <b>{new_bal} CPS</b></p>
            <p>Best regards,</p>
            <p>Sellangle Team</p>
        </body>
        </html>
    """
    inbox_message = SendMessageInbox.objects.create(
        receiver=user,
        subject="CPS Transaction",
        message=message_content,
        is_read=False,
    )
    inbox_message.msg_count += 1
    inbox_message.save()
    print(f"Notification sent to {user.username} about CPS Transaction.")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def buy_credit_point(request):
    user = request.user
    amount = Decimal(request.data.get('amount'))
    currency = request.data.get('currency')
    created_at = request.data.get('created_at')
    print('amount:', amount, currency)

    try:
        if currency == "NGN": 
            cps_purchase_id = generate_cps_purchase_id()
            print('cps_purchase_id:', cps_purchase_id)

            AMOUNT_TO_CPS_MAPPING = {
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
            print('amount:', amount, 'cps_amount:', cps_amount)

            try:
                credit_point, created = CreditPoint.objects.get_or_create(user=user)
                old_bal = credit_point.balance
                print('cps old_bal):', old_bal)

                credit_point.balance += cps_amount
                credit_point.save()

                buy_credit_point = BuyCreditPoint.objects.create( 
                    user=user,
                    amount=amount,
                    cps_purchase_id=cps_purchase_id,
                    cps_amount=cps_amount,
                    old_bal=old_bal,
                )
                buy_credit_point.is_success = True
                buy_credit_point.new_bal = credit_point.balance
                buy_credit_point.save()
                print('cps balance(after):', credit_point.balance)

                new_bal = credit_point.balance
                # send mgs
                amount = '{:,.0f}'.format(float(amount))
                cps_amount = '{:,.0f}'.format(cps_amount)
                old_bal = '{:,.0f}'.format(old_bal)
                new_bal = '{:,.0f}'.format(new_bal)

                try:
                    send_buy_cps_msg_alert_to_buyer(request, user, amount, currency, old_bal, new_bal, cps_amount)
                except Exception as e:
                    print(e)
                    return Response({'error': 'Error sending notification.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                return Response({'detail': f'Credit point request successful.'}, status=status.HTTP_201_CREATED)
            except CreditPoint.DoesNotExist:
                    return Response({'detail': 'Credit point not found'}, status=status.HTTP_404_NOT_FOUND)
            
        elif currency == "USD":
            usd_cps_purchase_id = generate_cps_purchase_id()
            print('cps_purchase_id:', usd_cps_purchase_id)
            
            AMOUNT_TO_CPS_MAPPING = {
            '1': 1000,
            '5': 5200,
            '10': 10800,
            '15': 16500,
            '20': 24000,
            '50': 60000,
            '100': 125000,
            '200': 255000,
            '500': 700000,
            '1000': 1500000,
            }

            cps_amount = AMOUNT_TO_CPS_MAPPING.get(str(amount), 0)
            print('amount:', amount, 'cps_amount:', cps_amount)

            try:
                credit_point, created = CreditPoint.objects.get_or_create(user=user)
                
                old_bal = credit_point.balance
                print('cps old_bal):', old_bal)

                credit_point.balance += cps_amount
                credit_point.save()

                buy_credit_point = BuyUsdCreditPoint.objects.create( 
                    user=user,
                    amount=amount,
                    usd_cps_purchase_id=usd_cps_purchase_id,
                    cps_amount=cps_amount,
                    old_bal=old_bal,
                )

                buy_credit_point.is_success = True
                buy_credit_point.new_bal = credit_point.balance
                buy_credit_point.save()
                print('cps balance(after):', credit_point.balance)

                new_bal = credit_point.balance
                # send mgs
                amount = '{:,.0f}'.format(float(amount))
                cps_amount = '{:,.0f}'.format(cps_amount)
                old_bal = '{:,.0f}'.format(old_bal)
                new_bal = '{:,.0f}'.format(new_bal)

                try:
                    send_buy_cps_msg_alert_to_buyer(request, user, amount, currency, old_bal, new_bal, cps_amount)
                except Exception as e:
                    print(e)
                    return Response({'error': 'Error sending email.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                return Response({'detail': f'Credit point request successful.'}, 
                                status=status.HTTP_201_CREATED)
            except CreditPoint.DoesNotExist:
                    return Response({'detail': 'Credit point not found'}, status=status.HTTP_404_NOT_FOUND)
        # elif currency == "EUR":
        #     buy_eur_credit_point(request, amount, currency, created_at)
        else:
            return Response({'detail': 'Invalid currency format. Please contact the seller.'}, status=status.HTTP_400_BAD_REQUEST)
        # return Response(status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'detail': 'Invalid API key. Please contact the seller.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sell_cps_to_sellangle(request):
    user = request.user
    data = request.data
    amount = Decimal(request.data.get('amount'))
    # cps_amount = Decimal(request.data.get('cps_amount'))
    currency = request.data.get('currency')
    created_at = request.data.get('created_at')
    print('amount:', amount, currency)

    buyer_username = data.get('username')
    password = data.get('password')

    if not user.check_password(password):
        return Response({'detail': 'Invalid password.'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        buyer = User.objects.get(username=buyer_username)
    except User.DoesNotExist:
        return Response({'detail': f'CPS Buyer/Receiver with username "{buyer_username}" not found.'}, status=status.HTTP_404_NOT_FOUND)
    print('buyer:', buyer)
    
    try:  
        if currency == "NGN": 
            sell_ngn_cps_to_sellangle(request, user, amount, currency, created_at)
        elif currency == "USD":
            sell_usd_cps_to_sellangle(request, user, amount, currency, created_at)
        # elif currency == "EUR":
        #     buy_eur_credit_point(request, amount, currency, created_at)
        else:
            return Response({'detail': 'Invalid currency format. Please contact the seller.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'detail': 'Invalid API key. Please contact the seller.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# # @transaction.atomic
# def buy_cps_in_ngn(request, user, amount, currency, created_at): 
#     cps_purchase_id = generate_cps_purchase_id()
#     print('cps_purchase_id:', cps_purchase_id)
#     print('cps_amount:', cps_amount)
#     print('currency:', currency)

#     AMOUNT_TO_CPS_MAPPING = {
#     '500': 500,
#     '1000': 1000,
#     '5000': 5200,
#     '10000': 10800,
#     '15000': 16500,
#     '20000': 24000,
#     '50000': 60000,
#     '100000': 125000,
#     '200000': 255000,
#     '500000': 700000,
#     '1000000': 1500000,
#     }

#     amount = 0
#     cps_amount = AMOUNT_TO_CPS_MAPPING.get(str(amount), 0)
#     print('amount:', amount, 'cps_amount:', cps_amount)

#     try:
#         credit_point, created = CreditPoint.objects.get_or_create(user=user)
#         old_bal = credit_point.balance
#         print('cps old_bal):', old_bal)

#         credit_point.balance += cps_amount
#         credit_point.save()

#         buy_credit_point = BuyCreditPoint.objects.create( 
#             user=user,
#             amount=amount,
#             cps_purchase_id=cps_purchase_id,
#             cps_amount=cps_amount,
#             old_bal=old_bal,
#         )
#         buy_credit_point.is_success = True
#         buy_credit_point.new_bal = credit_point.balance
#         buy_credit_point.save()
#         print('cps balance(after):', credit_point.balance)
#         return Response({'detail': f'Credit point request successful.'}, 
#                         status=status.HTTP_201_CREATED)
#     except CreditPoint.DoesNotExist:
#             return Response({'detail': 'Credit point not found'}, status=status.HTTP_404_NOT_FOUND)
    
#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# # @transaction.atomic
# def buy_cps_in_usd(request, user, amount, currency, created_at):
#     usd_cps_purchase_id = generate_cps_purchase_id()
#     print('cps_purchase_id:', usd_cps_purchase_id)
    
#     AMOUNT_TO_CPS_MAPPING = {
#     '1': 1000,
#     '5': 5200,
#     '10': 10800,
#     '15': 16500,
#     '20': 24000,
#     '50': 60000,
#     '100': 125000,
#     '200': 255000,
#     '500': 700000,
#     '1000': 1500000,
#     }

#     cps_amount = AMOUNT_TO_CPS_MAPPING.get(str(amount), 0)
#     print('amount:', amount, 'cps_amount:', cps_amount)

#     try:
#         credit_point, created = CreditPoint.objects.get_or_create(user=user)
        
#         old_bal = credit_point.balance
#         print('cps old_bal):', old_bal)

#         credit_point.balance += cps_amount
#         credit_point.save()

#         buy_credit_point = BuyUsdCreditPoint.objects.create( 
#             user=user,
#             amount=amount,
#             usd_cps_purchase_id=usd_cps_purchase_id,
#             cps_amount=cps_amount,
#             old_bal=old_bal,
#         )

#         buy_credit_point.is_success = True
#         buy_credit_point.new_bal = credit_point.balance
#         buy_credit_point.save()
#         print('cps balance(after):', credit_point.balance)

#         return Response({'detail': f'Credit point request successful.'}, 
#                         status=status.HTTP_201_CREATED)
#     except CreditPoint.DoesNotExist:
#             return Response({'detail': 'Credit point not found'}, status=status.HTTP_404_NOT_FOUND)
#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def sell_ngn_cps_to_sellangle(request, user, amount, currency, created_at):
    seller_username='sellangle'
    seller = User.objects.get(username=seller_username)

    NGN_AMOUNT_TO_CPS_MAPPING = {
    '1000000': 2000000,
    '2500000': 5000000,
    '5000000': 10000000,
    '7500000': 15000000,
    '10000000': 20000000,
    }

    cps_sell_id = generate_cps_sell_id()
    print('cps_sell_id:', cps_sell_id)

    # buyer_username = data.get('username')
    # password = data.get('password')

    # if not seller.check_password(password):
    #     return Response({'detail': 'Invalid password.'}, status=status.HTTP_401_UNAUTHORIZED)

    # try:
    #     buyer = User.objects.get(username=buyer_username)
    # except User.DoesNotExist:
    #     return Response({'detail': f'CPS Buyer/Receiver with username "{buyer_username}" not found.'}, status=status.HTTP_404_NOT_FOUND)
    # print('buyer:', buyer)

    try:
        seller_credit_point, created = CreditPoint.objects.get_or_create(user=seller)
        seller_old_bal = seller_credit_point.balance

        buyer_credit_point, created = CreditPoint.objects.get_or_create(user=buyer)
        buyer_old_bal = buyer_credit_point.balance

        sell_credit_point = SellCreditPoint.objects.create(
            buyer=buyer,
            seller=seller,
            amount=amount,
            buyer_old_bal=buyer_old_bal,
            seller_old_bal=seller_old_bal,
            cps_sell_id=cps_sell_id, 
        )
        
        if seller_old_bal < amount: 
            return Response({'detail': 'Insufficient credit point balance. Fund your cps wallet and try again.'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        seller_credit_point.balance -= amount
        seller_credit_point.save()
        
        buyer_credit_point.balance += amount
        buyer_credit_point.save()

        sell_credit_point.is_success = True
        sell_credit_point.buyer_new_bal = buyer_credit_point.balance 
        sell_credit_point.seller_new_bal = seller_credit_point.balance
        sell_credit_point.save()

        return Response({'detail': f'Credit point request successful.'}, 
                        status=status.HTTP_201_CREATED)
    except CreditPoint.DoesNotExist:
            return Response({'detail': 'Credit point not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def sell_usd_cps_to_sellangle(request, user, amount, currency, created_at):
    seller_username='sellangle'
    seller = User.objects.get(username=seller_username)
    data = request.data
    print('data:', data)

    USD_AMOUNT_TO_CPS_MAPPING = {
    '1000': 2000000,
    '2500': 5000000,
    '5000': 10000000,
    '7500': 15000000,
    '10000': 20000000,
    }

    cps_sell_id = generate_cps_sell_id()
    print('cps_sell_id:', cps_sell_id)

    # buyer_username = data.get('username')
    # password = data.get('password')

    # if not seller.check_password(password):
    #     return Response({'detail': 'Invalid password.'}, status=status.HTTP_401_UNAUTHORIZED)

    # try:
    #     buyer = User.objects.get(username=buyer_username)
    # except User.DoesNotExist:
    #     return Response({'detail': f'CPS Buyer/Receiver with username "{buyer_username}" not found.'}, status=status.HTTP_404_NOT_FOUND)
    # print('buyer:', buyer)

    try:
        seller_credit_point, created = CreditPoint.objects.get_or_create(user=seller)
        seller_old_bal = seller_credit_point.balance

        buyer_credit_point, created = CreditPoint.objects.get_or_create(user=buyer)
        buyer_old_bal = buyer_credit_point.balance

        sell_credit_point = SellCreditPoint.objects.create(
            buyer=buyer,
            seller=seller,
            amount=amount,
            buyer_old_bal=buyer_old_bal,
            seller_old_bal=seller_old_bal,
            cps_sell_id=cps_sell_id, 
        )
        
        if seller_old_bal < amount: 
            return Response({'detail': 'Insufficient credit point balance. Fund your cps wallet and try again.'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        seller_credit_point.balance -= amount
        seller_credit_point.save()
        
        buyer_credit_point.balance += amount
        buyer_credit_point.save()

        sell_credit_point.is_success = True
        sell_credit_point.buyer_new_bal = buyer_credit_point.balance 
        sell_credit_point.seller_new_bal = seller_credit_point.balance
        sell_credit_point.save()

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
        seller_credit_point, created = CreditPoint.objects.get_or_create(user=seller)
        seller_old_bal = seller_credit_point.balance

        buyer_credit_point, created = CreditPoint.objects.get_or_create(user=buyer)
        buyer_old_bal = buyer_credit_point.balance

        sell_credit_point = SellCreditPoint.objects.create(
            buyer=buyer,
            seller=seller,
            amount=amount,
            buyer_old_bal=buyer_old_bal,
            seller_old_bal=seller_old_bal,
            cps_sell_id=cps_sell_id, 
        )
        
        if seller_old_bal < amount: 
            return Response({'detail': 'Insufficient credit point balance. Fund your cps wallet and try again.'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        seller_credit_point.balance -= amount
        seller_credit_point.save()
        
        buyer_credit_point.balance += amount
        buyer_credit_point.save()

        sell_credit_point.is_success = True
        sell_credit_point.buyer_new_bal = buyer_credit_point.balance 
        sell_credit_point.seller_new_bal = seller_credit_point.balance
        sell_credit_point.save()

        return Response({'detail': f'Credit point request successful.'}, 
                        status=status.HTTP_201_CREATED)
    except CreditPoint.DoesNotExist:
            return Response({'detail': 'Credit point not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_credit_points_balance_view(request):
    try:
        credit_point, created = CreditPoint.objects.get_or_create(user=request.user)
        serializer = CreditPointSerializer(credit_point)
        return Response(serializer.data)
    except CreditPoint.DoesNotExist:
        return Response({'detail': 'Credit point balance not found'}, status=status.HTTP_404_NOT_FOUND)


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
def get_usd_buy_credit_point(request):
    user = request.user
    try:
        credit_point = BuyUsdCreditPoint.objects.filter(user=user).order_by('-created_at')
        serializer = BuyUsdCreditPointSerializer(credit_point, many=True) 
        return Response(serializer.data)
    except BuyUsdCreditPoint.DoesNotExist:
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_ad_charges_cps(request):
    user = request.user
    try:
        credit_point = AdChargeCreditPoint.objects.filter(user=user).order_by('-created_at')
        serializer = AdChargeCreditPointSerializer(credit_point, many=True)
        return Response(serializer.data)
    except AdChargeCreditPoint.DoesNotExist:
        return Response({'detail': 'Credit point not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_cps_bonuses(request):
    user = request.user
    try:
        credit_point = CpsBonus.objects.filter(user=user).order_by('-created_at')
        serializer = CpsBonusSerializer(credit_point, many=True) 
        return Response(serializer.data)
    except CpsBonus.DoesNotExist:
        return Response({'detail': 'Credit point not found'}, status=status.HTTP_404_NOT_FOUND)
