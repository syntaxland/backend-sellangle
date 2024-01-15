# promo/views.py
import random
import string
import requests
from decimal import Decimal

from django.shortcuts import get_object_or_404
from django.conf import settings
from django.http import JsonResponse
from django.http import Http404
from django.db.models import Sum

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
# from paystack.resource import TransactionResource
from app.models import Product, Order
from payment.models import Payment
from .serializers import PaymentSerializer, UserPaymentSerializer
from credit_point.models import CreditPoint, CreditPointPayment, CreditPointEarning
from promo.models import Referral, ReferralBonus
from django.contrib.auth import get_user_model

User = get_user_model()

def generate_payment_reference():
    return ''.join(random.choices(string.digits, k=10))


class PaymentDetailsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        paystack_public_key = settings.PAYSTACK_PUBLIC_KEY
        paysofter_public_key = settings.PAYSOFTER_PUBLIC_KEY

        # email = request.user.email
        reference = generate_payment_reference()
        print("paystack_public_key:", paystack_public_key, "paysofter_public_key:", paysofter_public_key, reference)
        # print(public_key, reference, email)
        return Response({
            "paystackPublicKey": paystack_public_key,
            "paysofterPublicKey": paysofter_public_key,  
            "reference": reference,
        #  "email": email,
            })
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_payment(request):
    user = request.user
    data = request.data
    try:
        amount = int(request.data.get('amount'))
        email = request.data.get('email')
        reference = data.get('reference')
        order_id = data.get('order_id')

        promo_code_discount_amount = Decimal(data.get('promo_code_discount_amount', 0))
        items_amount = data.get('items_amount', 0) 
        final_items_amount = data.get('final_items_amount', 0) 
        promo_code_discount_percentage = data.get('promo_code_discount_percentage', 0)
        final_total_amount = data.get('final_total_amount', 0)

        print('Payment Details:','Amount:', amount,'Reference:', 
              reference, 'Order ID:', order_id, 'Email:', email)
        if not order_id:
            return Response({'detail': 'Order ID not found.'}, status=status.HTTP_400_BAD_REQUEST)

        
        # Associate the payment with the corresponding order
        try:
            order = Order.objects.get(order_id=order_id)
            # order = Order.objects.get(order_id=order_id)

            # Create the Payment instance
            payment = Payment.objects.create(
                user=user,
                reference=reference,
                amount=amount,
                order=order,

                promo_code_discount_amount=promo_code_discount_amount,
                items_amount=items_amount,
                final_items_amount=final_items_amount,
                promo_code_discount_percentage=promo_code_discount_percentage,
                final_total_amount=final_total_amount,
            )

            order.isPaid = True
            order.paidAt = payment.created_at
            order.save()

            payment.save()
            print('Payment details:', payment)

            # Calculate the credit points earned (1% and/or 0.5% of payment final_items_amount)
            credit_points_earned = Decimal(str(final_items_amount)) * Decimal('0.01')
            referral_credit_points_bonus = Decimal(str(final_items_amount)) * Decimal('0.005')
            print('Credit_points_earned:', credit_points_earned,
                  'Referral_credit_points_bonus:', referral_credit_points_bonus, 
                  'Final items amount:', final_items_amount,
                  'Total amount:', amount,
                  'Final total amount after promo:', final_total_amount,
                )
            try:
                # Get or create the user's credit point balance
                credit_point, created = CreditPoint.objects.get_or_create( 
                    user=request.user,
                    )
                
                credit_point.balance += credit_points_earned
                credit_point.save()
                print('Credit points added.')

                try:
                    CreditPointEarning.objects.create(
                    user=request.user,
                    order_payment=payment,
                    credit_points_earned=credit_points_earned, 
                    )
                except CreditPointEarning.DoesNotExist:
                    pass

                print('Getting referrals...')
                referrals = Referral.objects.filter(referred_users=user)
                if not referrals:
                        return Response({'detail': 'Referrer not found.'})
                
                for referral in referrals:
                    print('Getting referrer...')
                    referrer = referral.referrer
                    print('referrer:', referrer)

                    print('\nGetting ReferralBonus...')

                    try:
                        # Check if a ReferralBonus for the same referrer already exists
                        existing_referral_bonus = ReferralBonus.objects.filter(referrer=referrer).first()

                        if existing_referral_bonus:
                            # If it exists, update the existing bonus
                            existing_referral_bonus.referral_credit_points_bonus += referral_credit_points_bonus
                            existing_referral_bonus.save()
                        else:
                            # If it doesn't exist, create a new one
                            ReferralBonus.objects.create(
                                referrer=referrer, 
                                referral_credit_points_bonus=referral_credit_points_bonus,
                            )
                        
                        # Update the referrer's credit point balance for each referral
                        referrer_credit_point, created = CreditPoint.objects.get_or_create(user=referrer)
                        referrer_credit_point.balance += referral_credit_points_bonus
                        referrer_credit_point.save()
                    except ReferralBonus.DoesNotExist:
                        pass
             
                print('Getting CreditPointPayment...')
                try:
                    CreditPointPayment.objects.create(
                        order_payment=payment,
                        referrer=referrer, 
                        credit_points_earned=credit_points_earned,
                        referral_credit_points_bonus=referral_credit_points_bonus,
                    )
                except CreditPointPayment.DoesNotExist:
                    return Response({'detail': 'Credit Point Payments not found.'}, status=status.HTTP_404_NOT_FOUND)
                
            except CreditPoint.DoesNotExist:
                pass
            
            # Return a success response
            return Response({'detail': 'Payment successful'}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            # return Response({'detail': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)
            pass
            
        serializer = PaymentSerializer(payment)
        return Response({'payment': serializer.data,}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_payments(request):
    user = request.user
    payments = Payment.objects.filter(user=user).order_by('-created_at') 
    serializer = PaymentSerializer(payments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
# @permission_classes([IsAdminUser])
@permission_classes([IsAuthenticated]) 
def get_all_payments_view(request):
    try:
        all_payments = Payment.objects.all().order_by('-created_at')
        serializer = PaymentSerializer(all_payments, many=True)
        return Response(serializer.data)
    except Payment.DoesNotExist:
        return Response({'detail': 'Credit point not found'}, status=status.HTTP_404_NOT_FOUND)
