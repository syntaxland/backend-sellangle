# marketplace/views.py
import random
import string
import base64
from io import BytesIO
from PIL import Image, ImageDraw
import qrcode
from decimal import ROUND_DOWN, Decimal
from xhtml2pdf import pisa 
# import xhtml2pdf.pisa as pisa
# from xhtml2pdf.pisa import CreatePDF 
from dateutil.relativedelta import relativedelta
from calendar import month_name
from datetime import datetime, timedelta

from django.utils import timezone
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.db.models import Sum, F
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
# from django.shortcuts import render
from django.views.generic import View

# from .utils import render_to_pdf
# import nltk
# from nltk.corpus import wordnet

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
 
# from send_email.send_email_sendinblue import send_email_with_attachment_sendinblue
from credit_point.models import CreditPoint, AdChargeCreditPoint
# from credit_point.serializer import AdChargeCreditPointSerializer
from user_profile.serializers import UserSerializer

from .models import (MarketPlaceSellerAccount,
                     MarketplaceSellerPhoto,
                     PostFreeAd, PostPaidAd,
                     PaysofterApiKey, Message,
                     ReportFreeAd, ReportPaidAd,
                     ReviewFreeAdSeller, ReviewPaidAdSeller,
                     FreeAdMessageId, PaidAdMessageId, AdChargeTotal,

                     )
from .serializers import (MarketPlaceSellerAccountSerializer,
                          MarketplaceSellerPhotoSerializer,
                          PostFreeAdSerializer, PostPaidAdSerializer,
                          PaysofterApiKeySerializer, MessageSerializer,
                          ReportFreeAdSerializer, ReportPaidAdSerializer,
                          ReviewFreeAdSellerSerializer, ReviewPaidAdSellerSerializer,
                          FreeAdMessageIdSerializer, PaidAdMessageIdSerializer, AdChargeTotalSerializer,
                          )

from user_profile.serializers import UserSerializer

from django.conf import settings
from django.db.models import Avg
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()


def generate_ad_message_id():
    return ''.join(random.choices(string.digits, k=20))


def generate_ad_charge_id():
    letters_and_digits = string.ascii_uppercase + string.digits
    return 'CHG'+''.join(random.choices(letters_and_digits, k=16))


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# @parser_classes([MultiPartParser, FormParser])
# def create_marketplace_seller(request):
#     data = request.data
#     print('data:', data)

#     seller, created = MarketPlaceSellerAccount.objects.get_or_create(
#         seller=request.user)
#     serializer = MarketPlaceSellerAccountSerializer(instance=seller, data=data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def create_marketplace_seller(request):
    try:
        data = request.data
        print('data:', data)

        seller, created = MarketPlaceSellerAccount.objects.get_or_create(
            seller=request.user)
        print('creating seller:', seller)
        serializer = MarketPlaceSellerAccountSerializer(
            instance=seller, data=data)
        if serializer.is_valid():
            serializer.save()
            print('created seller a/c!:')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('serializer.errors:', serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print('Error:', str(e))
        return Response({'detail': 'An error occurred while creating the marketplace seller.'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def create_marketplace_seller_photo(request):
    seller = request.user
    data = request.data
    print('seller:', seller)
    print('data:', data)
    photo, created = MarketplaceSellerPhoto.objects.get_or_create(
        seller=seller)
    serializer = MarketplaceSellerPhotoSerializer(instance=photo, data=data)
    if serializer.is_valid():
        serializer.save()

        seller.is_marketplace_seller = True
        seller.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def create_free_ad(request):
    seller = request.user
    data = request.data
    serializer = PostFreeAdSerializer(data=data)

    try:
        free_ad_count = PostFreeAd.objects.filter(seller=seller).count()
        print('free_ad_count:', free_ad_count)
        print('data:', data)

        if free_ad_count >= 3:
            return Response(
                {'detail': f'You can only post a maximum of 3 free ads. You have posted {free_ad_count} free ads.'},
                status=status.HTTP_400_BAD_REQUEST
            )
    except User.DoesNotExist:
        return Response({'detail': 'User does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

    print('\nMaximum of 3 free ads not exceeded...')

    if serializer.is_valid():
        try:
            ad = serializer.save(seller=seller)
            print('\nSerializer is valid...')

            if ad.duration:
                durations_mapping = {
                    '0 day': timedelta(hours=0),
                    '1 day': timedelta(hours=24),
                    '2 days': timedelta(days=2),
                    '3 days': timedelta(days=3),
                    '5 days': timedelta(days=5),
                    '1 week': timedelta(weeks=1),
                    '2 weeks': timedelta(weeks=2),
                    '1 month': timedelta(days=30),
                }

                ad.duration_hours = durations_mapping.get(
                    ad.duration, timedelta(hours=0))
                ad.expiration_date = timezone.now() + ad.duration_hours

            ad.is_active = True
            ad.save()
            print('\nAd created successfully:', ad)

            return Response({'success': 'Ad created successfully.'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print('Error during ad creation:', str(e))
            return Response({'detail': 'An error occurred during ad creation. Please try again.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR
                            )
    else:
        print('Serializer errors:', serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def create_paid_ad(request):
    seller = request.user
    data = request.data
    serializer = PostPaidAdSerializer(data=data)

    try:
        credit_point = CreditPoint.objects.get(user=seller)
        credit_point_balance = credit_point.balance

        print('credit_point_balance:', credit_point_balance)
        if credit_point_balance < 28.8:
            return Response({'detail': f'Your credit point credit point balance of {credit_point_balance} is too low. You need at least 28.8 cps to place a paid ad.'},
                            status=status.HTTP_400_BAD_REQUEST)
    except CreditPoint.DoesNotExist:
        pass

    if seller.ad_charge_is_owed == True:
        return Response({'detail': 'You have unpaid ad charges. Please fund your CPS Wallet and try again.'},
                        status=status.HTTP_400_BAD_REQUEST)

    if serializer.is_valid():
        ad = serializer.save(seller=seller)

        if ad.duration:
            durations_mapping = {
                '0 day': timedelta(hours=0),
                '1 day': timedelta(hours=24),
                '2 days': timedelta(days=2),
                '3 days': timedelta(days=3),
                '5 days': timedelta(days=5),
                '1 week': timedelta(weeks=1),
                '2 weeks': timedelta(weeks=2),
                '1 month': timedelta(days=30),
            }

            ad.duration_hours = durations_mapping.get(
                ad.duration, timedelta(hours=0))
            ad.expiration_date = timezone.now() + ad.duration_hours

        ad.is_active = True
        ad.save()

        return Response({'success': f'Ad created successfully.'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def get_marketplace_seller_account(request):
    user = request.user
    try:
        marketplace_seller_account = MarketPlaceSellerAccount.objects.get(
            seller=user)
        serializer = MarketPlaceSellerAccountSerializer(
            marketplace_seller_account)
        return Response(serializer.data)
    except MarketPlaceSellerAccount.DoesNotExist:
        return Response({'detail': 'Marketplace seller account not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def update_marketplace_seller_account(request):
    user = request.user
    data = request.data
    print('data:', data)
    try:
        marketplace_seller_account = MarketPlaceSellerAccount.objects.get(
            seller=user)
    except MarketPlaceSellerAccount.DoesNotExist:
        return Response({'detail': 'Marketplace seller account not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = MarketPlaceSellerAccountSerializer(
        marketplace_seller_account, data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'detail': 'Marketplace seller account updated successfully.'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def get_marketplace_seller_photo(request):
    user = request.user
    try:
        marketplace_seller_photo = MarketplaceSellerPhoto.objects.get(
            seller=user)
        serializer = MarketplaceSellerPhotoSerializer(marketplace_seller_photo)
        return Response(serializer.data)
    except MarketplaceSellerPhoto.DoesNotExist:
        return Response({'detail': 'Marketplace seller photo not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def update_marketplace_seller_photo(request):
    user = request.user
    data = request.data
    print('data:', data)
    try:
        marketplace_seller_photo = MarketplaceSellerPhoto.objects.get(
            seller=user)
    except MarketplaceSellerPhoto.DoesNotExist:
        return Response({'detail': 'Marketplace seller photo not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = MarketplaceSellerPhotoSerializer(
        marketplace_seller_photo, data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'detail': 'Marketplace seller photo updated successfully.'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_seller_ad_statistics(request):
    user = request.user
    print('user:', user)
    try:
        free_ad_views = PostFreeAd.objects.filter(seller=user).aggregate(
            total_views=Sum('ad_view_count'))['total_views'] or 0
        paid_ad_views = PostPaidAd.objects.filter(seller=user).aggregate(
            total_views=Sum('ad_view_count'))['total_views'] or 0
        free_ad_saved = PostFreeAd.objects.filter(seller=user).aggregate(
            total_saved=Sum('ad_save_count'))['total_saved'] or 0
        paid_ad_saved = PostPaidAd.objects.filter(seller=user).aggregate(
            total_saved=Sum('ad_save_count'))['total_saved'] or 0
        followers_count = MarketPlaceSellerAccount.objects.filter(seller=user).aggregate(
            total_followers_count=Sum('follow_seller_count'))['total_followers_count'] or 0

        total_views = free_ad_views + paid_ad_views
        total_saved = free_ad_saved + paid_ad_saved
        total_followers_count = followers_count
        print('total_views:', total_views)
        print('total_followers_count:', total_followers_count)

        return Response({
            'totalSellerAdsViews': total_views,
            'totalSellerAdSaved': total_saved,
            'totalFollwersCount': total_followers_count,
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def toggle_follow_seller(request):
#     user = request.user
#     data = request.data

#     seller_username = data.get('seller_username')
#     seller = User.objects.get(username=seller_username)

#     print("seller:", seller)
#     print("data:", data)

#     try:
#         seller_account = MarketPlaceSellerAccount.objects.get(seller=seller)
#     except MarketPlaceSellerAccount.DoesNotExist:
#         return Response({'error': 'Seller account does not exist'}, status=status.HTTP_404_NOT_FOUND)

#     if seller_account in seller.seller_followers.all():
#         seller.seller_followers.remove(seller_account)
#         seller_account.follow_seller_count -= 1
#         user.followed_sellers.remove(seller_account)
#         print("removed")
#     else:
#         seller.seller_followers.add(seller_account)
#         seller_account.follow_seller_count += 1
#         user.followed_sellers.add(seller_account)
#         print("added")

#     user.save()
#     seller_account.save()

#     serializer = MarketPlaceSellerAccountSerializer(seller_account)
#     return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_follow_seller(request):
    user = request.user
    data = request.data

    seller_username = data.get('seller_username')
    seller = User.objects.get(username=seller_username)

    print("seller:", seller)
    print("data:", data)

    try:
        seller_account = MarketPlaceSellerAccount.objects.get(seller=seller)
    except MarketPlaceSellerAccount.DoesNotExist:
        return Response({'error': 'Seller account does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if seller_account in user.followed_sellers.all():
        user.followed_sellers.remove(seller_account)
        seller_account.follow_seller_count -= 1
        print("removed")
    else:
        user.followed_sellers.add(seller_account)
        seller_account.follow_seller_count += 1
        print("added")

    user.save()
    seller_account.save()

    serializer = MarketPlaceSellerAccountSerializer(seller_account)
    return Response(serializer.data)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_followed_sellers(request):
#     user = request.user
#     print("user:", user)

#     try:
#         seller_avatar = MarketplaceSellerPhoto.objects.get(seller=seller)
#         seller_avatar_url = seller_avatar.photo.url
#     except MarketplaceSellerPhoto.DoesNotExist:
#         seller_avatar_url = None

#     try:
#         followed_sellers = user.followed_sellers.all()
#         serializer = MarketPlaceSellerAccountSerializer(followed_sellers, many=True)

#         return Response({'data': serializer.data,
#                          'seller_avatar_url': seller_avatar_url,
#                          },
#                         status=status.HTTP_200_OK)

#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_followed_sellers(request):
    user = request.user
    print("user:", user)

    try:
        followed_sellers = user.followed_sellers.all()
        serializer = MarketPlaceSellerAccountSerializer(
            followed_sellers, many=True)

        followed_sellers_data = []
        for seller_data in serializer.data:
            seller_id = seller_data['seller']
            try:
                seller_avatar = MarketplaceSellerPhoto.objects.get(
                    seller_id=seller_id)
                seller_avatar_url = seller_avatar.photo.url
            except MarketplaceSellerPhoto.DoesNotExist:
                seller_avatar_url = None
            seller_data['seller_avatar_url'] = seller_avatar_url
            followed_sellers_data.append(seller_data)

        return Response({'data': followed_sellers_data}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def get_seller_free_ad(request):
    user = request.user
    # current_datetime = timezone.now()
    try:
        free_ad = PostFreeAd.objects.filter(seller=user)
        # free_ad = PostFreeAd.objects.filter(seller=user, expiration_date__gt=current_datetime)
        serializer = PostFreeAdSerializer(free_ad, many=True)
        return Response(serializer.data)
    except PostFreeAd.DoesNotExist:
        return Response({'detail': 'Free ad not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([AllowAny])
# @parser_classes([MultiPartParser, FormParser])
def get_seller_active_free_ads(request, seller_username):
    seller = User.objects.get(username=seller_username)
    print('seller_username:', seller_username)

    current_datetime = timezone.now()

    try:
        free_ad = PostFreeAd.objects.filter(
            seller=seller, expiration_date__gt=current_datetime)
        serializer = PostFreeAdSerializer(free_ad, many=True)
        return Response(serializer.data)
    except PostFreeAd.DoesNotExist:
        return Response({'detail': 'Free ad not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def get_free_ad_detail(request, pk):
    seller_api_key = None

    try:
        ad = PostFreeAd.objects.get(id=pk)
        seller = ad.seller

        try:
            api_key = PaysofterApiKey.objects.get(seller=seller)
            seller_api_key = api_key.live_api_key
        except PaysofterApiKey.DoesNotExist:
            seller_api_key = None
            # return Response({'detail': 'PaysofterApiKey not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            seller_avatar = MarketplaceSellerPhoto.objects.get(seller=seller)
            seller_avatar_url = seller_avatar.photo.url
        except MarketplaceSellerPhoto.DoesNotExist:
            seller_avatar_url = None

        try:
            seller_info = MarketPlaceSellerAccount.objects.get(seller=seller)
            is_seller_verified = seller_info.is_seller_verified
            seller_rating = seller_info.rating
            seller_review_count = seller_info.review_count
        except MarketPlaceSellerAccount.DoesNotExist:
            is_seller_verified = None

        # serializer = PostPaidAdSerializer(ad, context={'seller_avatar_url': seller_avatar_url})

        serializer = PostFreeAdSerializer(ad)
        return Response({'data': serializer.data,
                         'sellerApiKey': seller_api_key,
                         'seller_avatar_url': seller_avatar_url,
                         'is_seller_verified': is_seller_verified,
                         'seller_rating': seller_rating,
                         'seller_review_count': seller_review_count,
                         },
                        status=status.HTTP_200_OK)
    except PostFreeAd.DoesNotExist:
        return Response({'detail': 'Ad not found'}, status=status.HTTP_404_NOT_FOUND)
    except PaysofterApiKey.DoesNotExist:
        return Response({'detail': 'PaysofterApiKey not found'}, status=status.HTTP_404_NOT_FOUND)
    except MarketplaceSellerPhoto.DoesNotExist:
        return Response({'detail': 'MarketplaceSellerPhoto not found'}, status=status.HTTP_404_NOT_FOUND)


# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# @parser_classes([MultiPartParser, FormParser])
# def update_seller_free_ad(request):
#     user = request.user
#     data = request.data
#     print('data:', data)

#     ad_id = data.get('ad_id')
#     try:
#         free_ad = MarketPlaceSellerAccount.objects.get(seller=user, id=ad_id)
#     except MarketPlaceSellerAccount.DoesNotExist:
#         return Response({'detail': 'Free ad not found'}, status=status.HTTP_404_NOT_FOUND)
#     serializer = MarketPlaceSellerAccountSerializer(free_ad, data, partial=True)
#     if serializer.is_valid():
#         serializer.save()
#         return Response({'detail': 'Free ad updated successfully.'}, status=status.HTTP_200_OK)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def update_seller_free_ad(request):
    user = request.user
    data = request.data

    ad_id = data.get('ad_id')
    print('data:', data)

    try:
        paid_ad = PostFreeAd.objects.get(seller=user, id=ad_id)
    except PostFreeAd.DoesNotExist:
        return Response({'detail': 'Free ad not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = PostFreeAdSerializer(paid_ad, data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({'detail': 'Free ad updated successfully.'}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deactivate_free_ad(request):
    user = request.user
    data = request.data
    print('user:', user)
    print('data:', data)

    ad_id = data.get('ad_id')
    keyword = data.get('keyword')

    if keyword != "deactivate":
        return Response({'detail': 'Invalid keyword entered.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        ad = PostFreeAd.objects.get(seller=user, id=ad_id)
    except PostFreeAd.DoesNotExist:
        return Response({'detail': 'Ad not found.'}, status=status.HTTP_404_NOT_FOUND)

    ad.duration = '0 day'

    try:
        if ad.duration:
            durations_mapping = {
                '0 day': timedelta(hours=0),
                '1 day': timedelta(hours=24),
                '2 days': timedelta(days=2),
                '3 days': timedelta(days=3),
                '5 days': timedelta(days=5),
                '1 week': timedelta(weeks=1),
                '2 weeks': timedelta(weeks=2),
                '1 month': timedelta(days=30),
            }

            ad.duration_hours = durations_mapping.get(
                ad.duration, timedelta(hours=0))
            ad.expiration_date = timezone.now() + ad.duration_hours

        ad.is_active = False
        ad.save()

        return Response({'success': f'Ad deactivated successfully.'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reactivate_free_ad(request):
    user = request.user
    data = request.data
    print('user:', user)
    print('data:', data)

    ad_id = data.get('ad_id')

    try:
        ad = PostFreeAd.objects.get(seller=user, id=ad_id)
    except PostFreeAd.DoesNotExist:
        return Response({'detail': 'Ad not found.'}, status=status.HTTP_404_NOT_FOUND)

    ad.duration = data.get('duration')

    try:
        if ad.duration:
            durations_mapping = {
                '0 day': timedelta(hours=0),
                '1 day': timedelta(hours=24),
                '2 days': timedelta(days=2),
                '3 days': timedelta(days=3),
                '5 days': timedelta(days=5),
                '1 week': timedelta(weeks=1),
                '2 weeks': timedelta(weeks=2),
                '1 month': timedelta(days=30),
            }

            ad.duration_hours = durations_mapping.get(
                ad.duration, timedelta(hours=0))
            ad.expiration_date = timezone.now() + ad.duration_hours

        ad.is_active = True
        ad.save()

        return Response({'success': f'Ad reactivated successfully.'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_free_ad(request):
    user = request.user
    data = request.data
    print('user:', user)
    print('data:', data)

    ad_id = data.get('ad_id')
    keyword = data.get('keyword')

    if keyword != "delete":
        return Response({'detail': 'Invalid keyword entered.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        ad = PostFreeAd.objects.get(seller=user, id=ad_id)
        ad.delete()
        return Response({'detail': 'Ad deleted successfully.'})
    except PostFreeAd.DoesNotExist:
        return Response({'detail': 'Ad not found.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser])
def get_all_free_ad(request):

    current_datetime = timezone.now()

    selected_country = request.GET.get('country', '')
    selected_state = request.GET.get('state', '')
    selected_city = request.GET.get('city', '')
    print('free location:', selected_country, selected_state, selected_city)

    try:
        free_ads = PostFreeAd.objects.filter(
            expiration_date__gt=current_datetime).order_by("?")

        if selected_country:
            free_ads = free_ads.filter(country=selected_country)
        if selected_state:
            free_ads = free_ads.filter(state_province=selected_state)
        if selected_city:
            free_ads = free_ads.filter(city=selected_city)

        serializer = PostFreeAdSerializer(free_ads, many=True)
        return Response(serializer.data)
    except PostFreeAd.DoesNotExist:
        return Response({'detail': 'Free ad not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def get_seller_paid_ad(request):
    user = request.user
    # current_datetime = timezone.now()
    try:
        paid_ad = PostPaidAd.objects.filter(seller=user)
        # paid_ad = PostPaidAd.objects.filter(seller=user, expiration_date__gt=current_datetime)
        serializer = PostPaidAdSerializer(paid_ad, many=True)
        return Response(serializer.data)
    except PostPaidAd.DoesNotExist:
        return Response({'detail': 'Paid ad not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_seller_active_paid_ads(request, seller_username):
    seller = User.objects.get(username=seller_username)
    print('seller_username:', seller_username) 

    current_datetime = timezone.now()
    try:
        paid_ad = PostPaidAd.objects.filter(
            seller=seller, expiration_date__gt=current_datetime)
        serializer = PostPaidAdSerializer(paid_ad, many=True)
        return Response(serializer.data)
    except PostPaidAd.DoesNotExist:
        return Response({'detail': 'Paid ad not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def get_paid_ad_detail(request, pk):
    seller_api_key = None

    try:
        ad = PostPaidAd.objects.get(id=pk)
        seller = ad.seller

        try:
            api_key = PaysofterApiKey.objects.get(seller=seller)
            seller_api_key = api_key.live_api_key
        except PaysofterApiKey.DoesNotExist:
            seller_api_key = None

        try:
            seller_avatar = MarketplaceSellerPhoto.objects.get(seller=seller)
            seller_avatar_url = seller_avatar.photo.url
        except MarketplaceSellerPhoto.DoesNotExist:
            seller_avatar_url = None

        try:
            seller_info = MarketPlaceSellerAccount.objects.get(seller=seller)
            is_seller_verified = seller.is_seller_account_verified 
            seller_rating = seller_info.rating
            seller_review_count = seller_info.review_count
        except MarketPlaceSellerAccount.DoesNotExist:
            is_seller_verified = None

        serializer = PostPaidAdSerializer(
            ad, context={'seller_avatar_url': seller_avatar_url})

        return Response({'data': serializer.data,
                         'sellerApiKey': seller_api_key,
                         'seller_avatar_url': seller_avatar_url,
                        'is_seller_verified': is_seller_verified,
                         'seller_rating': seller_rating,
                         'seller_review_count': seller_review_count,
                         },
                        status=status.HTTP_200_OK)
    except PostPaidAd.DoesNotExist:
        return Response({'detail': 'Ad not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def update_seller_paid_ad(request):
    user = request.user
    data = request.data

    ad_id = data.get('ad_id')
    print('data:', data)

    try:
        credit_point = CreditPoint.objects.get(user=user)
        credit_point_balance = credit_point.balance

        print('credit_point_balance:', credit_point_balance)
        if credit_point_balance < 28.8:
            return Response({'detail': f'Your credit point credit point balance of {credit_point_balance} is too low. You need at least 28.8 cps to complete this action.'},
                            status=status.HTTP_400_BAD_REQUEST)
    except CreditPoint.DoesNotExist:
        pass

    if user.ad_charge_is_owed == True:
        return Response({'detail': 'You have unpaid ad charges. Please fund your CPS Wallet and try again.'},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        paid_ad = PostPaidAd.objects.get(seller=user, id=ad_id)
    except PostPaidAd.DoesNotExist:
        return Response({'detail': 'Paid ad not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = PostPaidAdSerializer(paid_ad, data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({'detail': 'Paid ad updated successfully.'}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deactivate_paid_ad(request):
    user = request.user
    data = request.data
    print('user:', user)
    print('data:', data)

    ad_id = data.get('ad_id')
    keyword = data.get('keyword')

    if keyword != "deactivate":
        return Response({'detail': 'Invalid keyword entered.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        ad = PostPaidAd.objects.get(seller=user, id=ad_id)
    except PostPaidAd.DoesNotExist:
        return Response({'detail': 'Ad not found.'}, status=status.HTTP_404_NOT_FOUND)

    ad.duration = '0 day'

    try:
        if ad.duration:
            durations_mapping = {
                '0 day': timedelta(hours=0),
                '1 day': timedelta(hours=24),
                '2 days': timedelta(days=2),
                '3 days': timedelta(days=3),
                '5 days': timedelta(days=5),
                '1 week': timedelta(weeks=1),
                '2 weeks': timedelta(weeks=2),
                '1 month': timedelta(days=30),
            }

            ad.duration_hours = durations_mapping.get(
                ad.duration, timedelta(hours=0))
            ad.expiration_date = timezone.now() + ad.duration_hours

        ad.is_active = False
        ad.save()

        return Response({'success': f'Ad deactivated successfully.'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reactivate_paid_ad(request):
    user = request.user
    data = request.data
    print('user:', user)
    print('data:', data)

    ad_id = data.get('ad_id')

    try:
        credit_point = CreditPoint.objects.get(user=user)
        credit_point_balance = credit_point.balance

        print('credit_point_balance:', credit_point_balance)
        if credit_point_balance < 28.8:
            return Response({'detail': f'Your credit point credit point balance of {credit_point_balance} is too low. You need at least 28.8 cps to complete this action.'},
                            status=status.HTTP_400_BAD_REQUEST)
    except CreditPoint.DoesNotExist:
        pass

    if user.ad_charge_is_owed == True:
        return Response({'detail': 'You have unpaid ad charges. Please fund your CPS Wallet and try again.'},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        ad = PostPaidAd.objects.get(seller=user, id=ad_id)
    except PostPaidAd.DoesNotExist:
        return Response({'detail': 'Ad not found.'}, status=status.HTTP_404_NOT_FOUND)

    ad.duration = data.get('duration')

    try:
        if ad.duration:
            durations_mapping = {
                '0 day': timedelta(hours=0),
                '1 day': timedelta(hours=24),
                '2 days': timedelta(days=2),
                '3 days': timedelta(days=3),
                '5 days': timedelta(days=5),
                '1 week': timedelta(weeks=1),
                '2 weeks': timedelta(weeks=2),
                '1 month': timedelta(days=30),
            }

            ad.duration_hours = durations_mapping.get(
                ad.duration, timedelta(hours=0))
            ad.expiration_date = timezone.now() + ad.duration_hours

        ad.is_active = True
        ad.save()

        return Response({'success': f'Ad reactivated successfully.'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_paid_ad(request):
    user = request.user
    data = request.data
    print('user:', user)
    print('data:', data)

    ad_id = data.get('ad_id')
    keyword = data.get('keyword')

    if keyword != "delete":
        return Response({'detail': 'Invalid keyword entered.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        ad = PostPaidAd.objects.get(seller=user, id=ad_id)
        ad.delete()
        return Response({'detail': 'Ad deleted successfully.'})
    except PostPaidAd.DoesNotExist:
        return Response({'detail': 'Ad not found.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser])
def get_all_paid_ad(request):

    current_datetime = timezone.now()

    selected_country = request.GET.get('country', '')
    selected_state = request.GET.get('state', '')
    selected_city = request.GET.get('city', '')

    # selected_category = request.GET.get('category', '')
    # selected_type = request.GET.get('type', '')
    print('paid location:', selected_country, selected_state, selected_city)

    try:
        paid_ads = PostPaidAd.objects.filter(
            expiration_date__gt=current_datetime).order_by("?")

        if selected_country:
            paid_ads = paid_ads.filter(country=selected_country)
        elif selected_state:
            paid_ads = paid_ads.filter(state_province=selected_state)
        elif selected_city:
            paid_ads = paid_ads.filter(city=selected_city)
        # elif selected_category:
        #     paid_ads = paid_ads.filter(ad_category=selected_category)
        # elif selected_type:
        #     paid_ads = paid_ads.filter(ad_type=selected_type)

        serializer = PostPaidAdSerializer(paid_ads, many=True)
        return Response(serializer.data)
    except PostPaidAd.DoesNotExist:
        return Response({'detail': 'Paid ad not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_seller_paid_ads_charges(request):
    user = request.user
    current_datetime = timezone.now()

    try:
        paid_ads = PostPaidAd.objects.filter(
            seller=user,
            ad_charges__gt=0
        ).exclude(
            expiration_date__lt=current_datetime,
            ad_charges=0
        )

        serializer_paid_ads = PostPaidAdSerializer(paid_ads, many=True)

        total_ad_charges = AdChargeTotal.objects.filter(seller=user).first()
        serializer_total_ad_charges = AdChargeTotalSerializer(total_ad_charges)

        response_data = {
            'ad_charges': serializer_paid_ads.data,
            'total_ad_charges': serializer_total_ad_charges.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)
    except PostPaidAd.DoesNotExist:
        return Response({'detail': 'Paid ad not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def pay_ad_charges(request):
    user = request.user
    data = request.data
    print('user:', user)
    print('data:', data)

    ad_charges_amt = Decimal(data.get('ad_charges_amt'))

    try:
        credit_point = CreditPoint.objects.get(user=user)
        credit_point_balance = credit_point.balance

        print('credit_point_balance:', credit_point_balance)
        if credit_point_balance < ad_charges_amt:
            return Response({'detail': f'Your credit point balance of {credit_point_balance} is too low. Please fund your CPS wallet and try again.'},
                            status=status.HTTP_400_BAD_REQUEST)

        CreditPoint.objects.get(user=user)
        credit_point.balance -= ad_charges_amt
        credit_point.save()

        credit_point = CreditPoint.objects.get(user=user)
        cps_new_bal = credit_point.balance

        AdChargeCreditPoint.objects.create(
            user=user,
            cps_amount=ad_charges_amt,
            old_bal=credit_point_balance,
            new_bal=cps_new_bal,
            ad_charge_cps_id=generate_ad_charge_id(),
            is_success=True,
        )

        ad_charges = AdChargeTotal.objects.get(seller=user)
        ad_charges.total_ad_charges = 0
        ad_charges.total_ad_charge_hours = 0
        ad_charges.save()

        PostPaidAd.objects.filter(
            seller=user,
            ad_charges__gt=0
        ).update(
            ad_charges=0,
            ad_charge_hours=0,
        )
        user.ad_charge_is_owed = False
        user.save()
    except CreditPoint.DoesNotExist:
        pass

    return Response({'success': f'Ad charged successfully.'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_ad_charges_receipt(request):
    user = request.user
    ad_charges_receipt_month_str = request.GET.get(
        'ad_charges_receipt_month', '')
    print('ad_charges_receipt_month_str:', ad_charges_receipt_month_str)

    ad_charges_receipt_month = datetime.strptime(
        ad_charges_receipt_month_str, '%B %Y')
    ad_charges_receipt_month_formatted = ad_charges_receipt_month.strftime(
        '%m/%Y')
    print('ad_charges_receipt_month_formatted:',
          ad_charges_receipt_month_formatted)

    try:
        pdf_data = generate_ad_charges_receipt_pdf(
            user, ad_charges_receipt_month_formatted)

        if pdf_data:
            # pdf_data_base64 = base64.b64encode(pdf_data).decode('utf-8')
            # # return HttpResponse(pdf_data_base64, content_type='text/plain')
            # return HttpResponse(pdf_data_base64, content_type='application/pdf')

            response = FileResponse(pdf_data, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{ad_charges_receipt_month_str}_ad_charges_receipt.pdf"'
            print('response:', response)
            return response

        else:
            return HttpResponse("Error generating ad charges receipt PDF", status=500)

    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)


def generate_ad_charges_receipt_pdf(user, ad_charges_receipt_month_formatted):
    print('ad_charges_receipt_month_formatted:',
          ad_charges_receipt_month_formatted)

    try:
        month, year = ad_charges_receipt_month_formatted.split('/')
        month = int(month)
        print('month:', month)
        print('year:', year)

        start_date = datetime(int(year), month, 1)
        end_date = (start_date + relativedelta(months=1)) - timedelta(days=1)
        print('start_date:', start_date)
        print('end_date:', end_date)

        ad_charges = AdChargeCreditPoint.objects.filter(
            user=user,
            created_at__range=(start_date, end_date),
            is_success=True
        ).values('created_at').annotate(total_ad_charges=Sum('cps_amount')).order_by('created_at')

        total_amount = ad_charges.aggregate(Sum('total_ad_charges'))[
            'total_ad_charges__sum']
        formatted_total_amount = '{:,.2f}'.format(
            float(total_amount) if total_amount is not None else 0.0)

        print('formatted_total_amount:', formatted_total_amount)

        context = {
            'user': user,
            'start_date': start_date.strftime('%B %d, %Y'),
            'end_date': end_date.strftime('%B %d, %Y'),
            'ad_charges': ad_charges,
            'account_id': 'Your Account ID Here',
            'bill_status': 'Issued',
            'date_printed': timezone.now().strftime('%b %d, %Y'),
            'formatted_total_amount': formatted_total_amount,
            'total_amount': total_amount,

        }
        # print('\ncontext:', context)

        template_path = 'marketplace/ad_charges_receipt.html'
        template = get_template(template_path)
        html = template.render(context)

        # # Create PDF data
        # pdf_content = BytesIO()
        # pisa.CreatePDF(html, dest=pdf_content)
        # pdf_content.seek(0)
        # pdf_data = pdf_content.getvalue()
        # pdf_content.close()
        # return pdf_data

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{ad_charges_receipt_month_formatted}_ad_charges_receipt.pdf"'
        pisa.CreatePDF(html, dest=response)
        return response

    except AdChargeCreditPoint.DoesNotExist: 
        return None


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def save_seller_paysofter_api_key(request):
    user = request.user
    data = request.data
    print('data:', data)

    api_key, created = PaysofterApiKey.objects.get_or_create(
        seller=request.user)
    # try:
    #     api_key = PaysofterApiKey.objects.get(seller=user)
    # except PaysofterApiKey.DoesNotExist:
    #     return Response({'detail': 'Api key not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = PaysofterApiKeySerializer(api_key, data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'detail': 'Api key updated successfully.'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_seller_paysofter_api_key(request):
    user = request.user
    try:
        api_key = PaysofterApiKey.objects.get(seller=user)
        serializer = PaysofterApiKeySerializer(api_key)
        return Response(serializer.data)
    except PaysofterApiKey.DoesNotExist:
        return Response({'detail': 'Api key not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def buyer_create_free_ad_message(request):
    user = request.user
    data = request.data
    print('data:', data, 'user:', user)

    ad_id = data.get('ad_id')
    message = data.get('message')
    print('message:', message)

    try:
        free_ad = PostFreeAd.objects.get(pk=ad_id)
    except PostFreeAd.DoesNotExist:
        return Response({'detail': 'Ad not found'}, status=status.HTTP_404_NOT_FOUND)

    free_ad_msg_id = FreeAdMessageId.objects.filter(
        user=user, free_ad=free_ad).first()
    if not free_ad_msg_id:
        free_ad_msg_id = FreeAdMessageId.objects.create(
            user=user,
            free_ad=free_ad,
            message=message,
            free_ad_message_id=generate_ad_message_id(),
        )

    free_ad_msg_id = FreeAdMessageId.objects.get(user=user, free_ad=free_ad)
    free_ad_id = free_ad_msg_id.free_ad_message_id
    print('free_ad_id:', free_ad_id)

    ad_message = Message.objects.create(
        buyer=user,
        message=message,
        free_ad=free_ad,
        free_ad_message_id=free_ad_msg_id,
    )

    if free_ad_msg_id:
        free_ad_msg_id.seller_free_ad_msg_count += 1
        free_ad_msg_id.message = message
        free_ad_msg_id.modified_at = timezone.now()
        free_ad_msg_id.save()

    return Response({'message': 'Message created'}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_free_ad_messages(request):
    user = request.user
    print('user:', user)

    ad_id = request.GET.get('ad_id', '')
    free_ad_message_id = request.GET.get('free_ad_message_id', '')
    print('ad_id:', ad_id)
    print('free_ad_message_id:', free_ad_message_id)

    try:
        free_ad = PostFreeAd.objects.get(id=ad_id)
    except PostFreeAd.DoesNotExist:
        return Response({'detail': 'Ad not found'}, status=status.HTTP_404_NOT_FOUND)
    # print('free_ad:', free_ad)

    try:
        # free_ad_msg_id = FreeAdMessageId.objects.get(free_ad=free_ad)
        free_ad_msg_id = FreeAdMessageId.objects.filter(
            free_ad=free_ad).first()
    except FreeAdMessageId.DoesNotExist:
        free_ad_msg_id = None

    if free_ad_msg_id:
        ad_message = Message.objects.filter(
            free_ad_message_id=free_ad_msg_id).order_by('timestamp')
        serializer = MessageSerializer(ad_message, many=True)
        return Response(serializer.data)
    else:
        return Response({'detail': 'No message(s) found or created yet.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def seller_reply_free_ad_message(request):
    seller = request.user
    data = request.data
    print('data:', data)

    ad_id = data.get('ad_id')
    message = data.get('message')
    free_ad_message_id = data.get('free_ad_message_id')
    print('free_ad_message_id:', free_ad_message_id)
    print('message:', message)

    try:
        free_ad = PostFreeAd.objects.get(pk=ad_id)
    except PostFreeAd.DoesNotExist:
        return Response({'detail': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        free_ad_msg_id = FreeAdMessageId.objects.get(
            free_ad=free_ad, free_ad_message_id=free_ad_message_id)
    except FreeAdMessageId.DoesNotExist:
        return Response({'detail': 'Ad ID not found'}, status=status.HTTP_404_NOT_FOUND)

    ad_message = Message.objects.create(
        seller=seller,
        message=message,
        free_ad=free_ad,
        free_ad_message_id=free_ad_msg_id,
    )

    if free_ad_msg_id:
        free_ad_msg_id.buyer_free_ad_msg_count += 1
        free_ad_msg_id.message = message
        free_ad_msg_id.modified_at = timezone.now()
        free_ad_msg_id.save()

    return Response({'message': 'Message created'}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_seller_free_ad_messages(request, pk):
    seller = request.user
    print('seller:', seller)

    try:
        free_ad = PostFreeAd.objects.get(pk=pk)
    except PostFreeAd.DoesNotExist:
        return Response({'detail': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        if free_ad:
            free_ad_msg_id = FreeAdMessageId.objects.get(free_ad=free_ad)
    except FreeAdMessageId.DoesNotExist:
        return Response({'detail': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)

    print('free_ad:', free_ad)

    try:
        if free_ad_msg_id:
            ad_message = Message.objects.filter(
                free_ad_message_id=free_ad_msg_id).order_by('timestamp')
            serializer = MessageSerializer(ad_message, many=True)
            return Response(serializer.data)
    except Message.DoesNotExist:
        return Response({'detail': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def buyer_create_paid_ad_message(request):
    user = request.user
    data = request.data
    print('data:', data, 'user:', user)

    ad_id = data.get('ad_id')
    message = data.get('message')
    print('message:', message)

    try:
        paid_ad = PostPaidAd.objects.get(pk=ad_id)
    except PostPaidAd.DoesNotExist:
        return Response({'detail': 'Ad not found'}, status=status.HTTP_404_NOT_FOUND)

    paid_ad_msg_id = PaidAdMessageId.objects.filter(
        user=user, paid_ad=paid_ad).first()
    if not paid_ad_msg_id:
        paid_ad_msg_id = PaidAdMessageId.objects.create(
            user=user,
            paid_ad=paid_ad,
            message=message,
            paid_ad_message_id=generate_ad_message_id(),
        )

    paid_ad_msg_id = PaidAdMessageId.objects.get(user=user, paid_ad=paid_ad)

    paid_ad_id = paid_ad_msg_id.paid_ad_message_id
    print('paid_ad_id:', paid_ad_id)

    ad_message = Message.objects.create(
        buyer=user,
        message=message,
        paid_ad=paid_ad,
        paid_ad_message_id=paid_ad_msg_id,
    )

    if paid_ad_msg_id:
        paid_ad_msg_id.seller_paid_ad_msg_count += 1
        paid_ad_msg_id.message = message
        paid_ad_msg_id.modified_at = timezone.now()
        paid_ad_msg_id.save()

    return Response({'message': 'Message created'}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_paid_ad_messages(request):
    user = request.user
    print('user:', user)

    ad_id = request.GET.get('ad_id', '')
    paid_ad_message_id = request.GET.get('paid_ad_message_id', '')
    print('paid_ad_message_id:', paid_ad_message_id)

    try:
        paid_ad = PostPaidAd.objects.get(pk=ad_id)
    except PostPaidAd.DoesNotExist:
        return Response({'detail': 'Ad not found'}, status=status.HTTP_404_NOT_FOUND)
    # print('paid_ad:', paid_ad)

    try:
        # paid_ad_msg_id = PaidAdMessageId.objects.get(paid_ad=paid_ad)
        paid_ad_msg_id = PaidAdMessageId.objects.filter(
            paid_ad=paid_ad).first()
    except PaidAdMessageId.DoesNotExist:
        paid_ad_msg_id = None

    if paid_ad_msg_id:
        ad_message = Message.objects.filter(
            paid_ad_message_id=paid_ad_msg_id).order_by('timestamp')
        serializer = MessageSerializer(ad_message, many=True)
        return Response(serializer.data)
    else:
        return Response({'detail': 'No message(s) found or created yet.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def seller_get_buyer_free_ad_messages(request):
    user = request.user
    print('user:', user)
    current_datetime = timezone.now()
    seller_free_ads = PostFreeAd.objects.filter(
        seller=user, expiration_date__gt=current_datetime)
    messages = FreeAdMessageId.objects.filter(
        free_ad__in=seller_free_ads).order_by('-modified_at')
    serializer = FreeAdMessageIdSerializer(messages, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def seller_get_buyer_paid_ad_messages(request):
    user = request.user
    print('user:', user)
    current_datetime = timezone.now()
    seller_paid_ads = PostPaidAd.objects.filter(
        seller=user, expiration_date__gt=current_datetime)
    messages = PaidAdMessageId.objects.filter(
        paid_ad__in=seller_paid_ads).order_by('-modified_at')
    serializer = PaidAdMessageIdSerializer(messages, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_active_buyer_free_ad_messages(request):
    user = request.user
    print('user:', user)
    current_datetime = timezone.now()
    messages = FreeAdMessageId.objects.filter(
        user=user,
        free_ad__expiration_date__gt=current_datetime
    ).order_by('-modified_at')
    serializer = FreeAdMessageIdSerializer(messages, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_active_buyer_paid_ad_messages(request):
    user = request.user
    print('user:', user)
    current_datetime = timezone.now()
    messages = PaidAdMessageId.objects.filter(
        user=user,
        paid_ad__expiration_date__gt=current_datetime
    ).order_by('-modified_at')
    serializer = PaidAdMessageIdSerializer(messages, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def seller_reply_paid_ad_message(request):
    seller = request.user
    data = request.data
    print('data:', data, 'seller:', seller)

    ad_id = data.get('ad_id')
    message = data.get('message')
    paid_ad_message_id = data.get('paid_ad_message_id')
    print('paid_ad_message_id:', paid_ad_message_id)
    print('message:', message)

    try:
        paid_ad = PostPaidAd.objects.get(pk=ad_id)
    except PostPaidAd.DoesNotExist:
        return Response({'detail': 'Ad not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        paid_ad_msg_id = PaidAdMessageId.objects.get(
            paid_ad=paid_ad, paid_ad_message_id=paid_ad_message_id)
    except PaidAdMessageId.DoesNotExist:
        return Response({'detail': 'Ad ID not found'}, status=status.HTTP_404_NOT_FOUND)

    ad_message = Message.objects.create(
        seller=seller,
        message=message,
        paid_ad=paid_ad,
        paid_ad_message_id=paid_ad_msg_id,
    )

    if paid_ad_msg_id:
        paid_ad_msg_id.buyer_paid_ad_msg_count += 1
        paid_ad_msg_id.message = message
        paid_ad_msg_id.modified_at = timezone.now()
        paid_ad_msg_id.save()

    return Response({'message': 'Message created'}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_seller_paid_ad_messages(request, pk):
    seller = request.user
    # data  = request.data
    # print('data:', data)
    print('seller:', seller)

    try:
        paid_ad = PostPaidAd.objects.get(pk=pk)
    except PostPaidAd.DoesNotExist:
        return Response({'detail': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        if paid_ad:
            paid_ad_msg_id = PaidAdMessageId.objects.get(paid_ad=paid_ad)
    except PaidAdMessageId.DoesNotExist:
        return Response({'detail': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)

    print('paid_ad:', paid_ad)

    try:
        if paid_ad_msg_id:
            ad_message = Message.objects.filter(
                paid_ad_message_id=paid_ad_msg_id,
            ).order_by('timestamp')
            serializer = MessageSerializer(ad_message, many=True)
            return Response(serializer.data)
    except Message.DoesNotExist:
        return Response({'detail': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([AllowAny])
def search_seller_username(request, seller_username):

    try:
        seller = User.objects.get(
            username=seller_username, is_marketplace_seller=True)
        serializer = UserSerializer(seller)

        try:
            seller_avatar = MarketplaceSellerPhoto.objects.get(seller=seller)
            seller_avatar_url = seller_avatar.photo.url
        except MarketplaceSellerPhoto.DoesNotExist:
            seller_avatar_url = None

        seller_detail = MarketPlaceSellerAccount.objects.get(seller=seller)
        serializer = MarketPlaceSellerAccountSerializer(seller_detail)
        return Response({'data': serializer.data, 'seller_avatar_url': seller_avatar_url}, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({'detail': 'Seller not found'}, status=status.HTTP_404_NOT_FOUND)
    except MarketPlaceSellerAccount.DoesNotExist:
        return Response({'detail': 'Seller detail not found'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_seller_shopfront_link(request):
    user = request.user
    url = settings.SELLANGLE_URL
    print("url:", url)
    print("user:", user)

    try:
        shopfront_link = f"{url}/shopfront/{user.username}/"
        print("shopfront_link:", shopfront_link)
        return Response({"shopfrontLink": shopfront_link}, status=status.HTTP_200_OK)
    except object.DoesNotExist:
        return Response({'detail': 'Link not found'}, status=status.HTTP_404_NOT_FOUND)
    # except Exception as e:
    #     return Response( {"error": str(e)},  status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser])
def get_seller_detail(request, seller_username):

    seller = User.objects.get(username=seller_username)

    try:
        seller_avatar = MarketplaceSellerPhoto.objects.get(seller=seller)
        seller_avatar_url = seller_avatar.photo.url
    except MarketplaceSellerPhoto.DoesNotExist:
        seller_avatar_url = None

    try:
        url = settings.SELLANGLE_URL
        shopfront_link = f"{url}/shopfront/{seller.username}/"
    except object.DoesNotExist:
        shopfront_link = None

    try:
        seller_detail = MarketPlaceSellerAccount.objects.get(seller=seller)
        serializer = MarketPlaceSellerAccountSerializer(seller_detail)

        return Response({'data': serializer.data, 
                         'seller_avatar_url': seller_avatar_url, 
                         'shopfront_link': shopfront_link
                         }, status=status.HTTP_200_OK)

    except MarketPlaceSellerAccount.DoesNotExist:
        return Response({'detail': 'Seller detail not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def report_free_ad(request):
    user = request.user
    data = request.data

    ad_id = data.get('ad_id')
    ad_report = data.get('ad_report')
    print("report data:", data)

    try:
        ad = PostFreeAd.objects.get(id=ad_id)
    except PostFreeAd.DoesNotExist:
        return Response({'detail': 'Ad not found.'}, status=status.HTTP_404_NOT_FOUND)

    report_ad, created = ReportFreeAd.objects.get_or_create(
        user=user,
        free_ad=ad,
        ad_report=ad_report,
    )

    ad.is_ad_reported = True
    ad.ad_report = ad_report
    ad.ad_report_count += 1
    ad.save()

    # if created:
    #     print("Report object was created:", report_ad)
    # else:
    #     print("Report object already existed:", report_ad)

    return Response({'success': f'Ad reported successfully.'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def report_paid_ad(request):
    user = request.user
    data = request.data

    ad_id = data.get('ad_id')
    ad_report = data.get('ad_report')
    print("report data:", data)

    try:
        ad = PostPaidAd.objects.get(id=ad_id)
    except PostPaidAd.DoesNotExist:
        return Response({'detail': 'Ad not found.'}, status=status.HTTP_404_NOT_FOUND)

    report_ad, created = ReportPaidAd.objects.get_or_create(
        user=user,
        paid_ad=ad,
        ad_report=ad_report,
    )

    ad.is_ad_reported = True
    ad.ad_report = ad_report
    ad.ad_report_count += 1
    ad.save()

    return Response({'success': f'Ad reported successfully.'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_free_ad_save(request):
    user = request.user
    data = request.data
    print("toggle_free_ad_save data:", data)

    ad_id = data.get('ad_id')

    if request.method == 'POST':
        ad = PostFreeAd.objects.get(pk=ad_id)

        if ad in user.saved_free_ads.all():
            user.saved_free_ads.remove(ad)
            ad.ad_is_saved = False
            ad.ad_save_count -= 1
        else:
            user.saved_free_ads.add(ad)
            ad.ad_is_saved = True
            ad.ad_save_count += 1

        user.save()
        ad.save()

        serializer = PostFreeAdSerializer(ad)
        return Response(serializer.data)
    else:
        return Response({'error': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_paid_ad_save(request):
    user = request.user
    data = request.data
    print("toggle_paid_ad_save data:", data)

    ad_id = data.get('ad_id')

    if request.method == 'POST':
        ad = PostPaidAd.objects.get(pk=ad_id)

        if ad in user.saved_paid_ads.all():
            user.saved_paid_ads.remove(ad)
            ad.ad_is_saved = False
            ad.ad_save_count -= 1
        else:
            user.saved_paid_ads.add(ad)
            ad.ad_is_saved = True
            ad.ad_save_count += 1

        user.save()
        ad.save()

        serializer = PostPaidAdSerializer(ad)
        return Response(serializer.data)
    else:
        return Response({'error': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def track_free_ad_view(request):
    user = request.user

    ad_id = request.data.get('ad_id')
    print("ad_id:", ad_id)

    try:
        ad = get_object_or_404(PostFreeAd, id=ad_id)
        if ad in user.viewed_free_ads.all():
            return Response({'message': 'Ad already viewed.'}, status=status.HTTP_200_OK)

        ad.ad_view_count += 1
        ad.save()

        user.viewed_free_ads.add(ad)

        return Response({'message': 'Ad viewed added successfully.'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def track_paid_ad_view(request):
    user = request.user

    ad_id = request.data.get('ad_id')
    print("ad_id:", ad_id)

    try:
        ad = get_object_or_404(PostPaidAd, id=ad_id)
        if ad in user.viewed_paid_ads.all():
            return Response({'message': 'Ad already viewed.'}, status=status.HTTP_200_OK)

        ad.ad_view_count += 1
        ad.save()

        user.viewed_paid_ads.add(ad)

        return Response({'message': 'Ad viewed added successfully.'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_viewed_free_ads(request):
    user = request.user
    print("user:", user)
    try:
        viewed_ads = user.viewed_free_ads.all()
        serializer = PostFreeAdSerializer(viewed_ads, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_viewed_paid_ads(request):
    user = request.user
    try:
        viewed_ads = user.viewed_paid_ads.all()
        serializer = PostPaidAdSerializer(viewed_ads, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_saved_free_ads(request):
    user = request.user
    try:
        saved_ads = user.saved_free_ads.all()
        serializer = PostFreeAdSerializer(saved_ads, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_saved_paid_ads(request):
    user = request.user
    try:
        saved_ads = user.saved_paid_ads.all()
        serializer = PostPaidAdSerializer(saved_ads, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def review_free_ad_seller(request):
    user = request.user
    data = request.data
    print("data:", data)

    ad_id = data.get('ad_id')
    rating = data.get('rating')
    comment = data.get('comment')

    if request.method == 'POST':
        ad = get_object_or_404(PostFreeAd, id=ad_id)
        seller = ad.seller

        # review = ReviewFreeAdSeller.objects.create(
        #     user=user,
        #     seller=seller,
        #     free_ad=ad,
        #     rating=rating,
        #     comment=comment,
        # )

        review, created = ReviewFreeAdSeller.objects.get_or_create(
            user=user,
            seller=seller,
            free_ad=ad,
            rating=rating,
            comment=comment,
        )

        reviews = ReviewFreeAdSeller.objects.filter(free_ad=ad)
        review.review_count = reviews.count()
        review.save()

        try:
            seller_account = MarketPlaceSellerAccount.objects.get(
                seller=seller)
            seller_account.rating = reviews.aggregate(Avg('rating'))[
                'rating__avg']
            seller_account.review_count = reviews.count()
            seller_account.save()
        except MarketPlaceSellerAccount.DoesNotExist:
            return Response({'detail': 'Seller account not found.'}, status=status.HTTP_404_NOT_FOUND)

        print("seller_account.rating:", seller_account.rating)

        serializer = ReviewFreeAdSellerSerializer(review, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def review_paid_ad_seller(request):
    user = request.user
    data = request.data
    print("data:", data)

    ad_id = data.get('ad_id')
    rating = data.get('rating')
    comment = data.get('comment')

    if request.method == 'POST':
        ad = get_object_or_404(PostPaidAd, id=ad_id)
        seller = ad.seller

        # review = ReviewPaidAdSeller.objects.create(
        #     user=user,
        #     seller=seller,
        #     paid_ad=ad,
        #     rating=rating,
        #     comment=comment,
        # )

        review, created = ReviewPaidAdSeller.objects.get_or_create(
            user=user,
            seller=seller,
            paid_ad=ad,
            rating=rating,
            comment=comment,
        )

        reviews = ReviewPaidAdSeller.objects.filter(paid_ad=ad)
        review.review_count = reviews.count()
        review.save()

        try:
            seller_account = MarketPlaceSellerAccount.objects.get(
                seller=seller)
            seller_account.rating = reviews.aggregate(Avg('rating'))[
                'rating__avg']
            seller_account.review_count = reviews.count()
            seller_account.save()
        except MarketPlaceSellerAccount.DoesNotExist:
            return Response({'detail': 'Seller account not found.'}, status=status.HTTP_404_NOT_FOUND)

        print("seller_account.rating:", seller_account.rating)

        serializer = ReviewPaidAdSellerSerializer(review, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_free_ad_review(request, review_id):
    user = request.user
    try:
        review = ReviewFreeAdSeller.objects.get(_id=review_id, user=user)
    except ReviewFreeAdSeller.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        rating = request.data.get('rating')
        comment = request.data.get('comment')

        # Check if the logged-in user is the same user who created the review
        if user == review.user:
            old_rating = review.rating  # Store the old rating for later adjustment
            review.rating = rating
            review.comment = comment
            review.save()

            # Update the rating and numReviews fields of the related product
            product = review.product
            reviews = ReviewFreeAdSeller.objects.filter(product=product)
            product.numReviews = reviews.count()
            product.rating = reviews.aggregate(Avg('rating'))['rating__avg']
            product.save()

            serializer = ReviewFreeAdSellerSerializer(review, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'You are not authorized to edit this review.'},
                            status=status.HTTP_403_FORBIDDEN)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @permission_classes([AllowAny])
def get_seller_free_ad_reviews(request):

    ad_id = request.GET.get('ad_id', '')
    print("ad_id:", ad_id)

    ad = get_object_or_404(PostFreeAd, id=ad_id)
    seller = ad.seller

    try:
        seller_avatar = MarketplaceSellerPhoto.objects.get(seller=seller)
        seller_avatar_url = seller_avatar.photo.url
    except MarketplaceSellerPhoto.DoesNotExist:
        seller_avatar_url = None

    try:
        review_list = ReviewFreeAdSeller.objects.filter(
            free_ad=ad).order_by('-timestamp')
        serializer = ReviewFreeAdSellerSerializer(review_list, many=True)
        return Response({'data': serializer.data,
                         'seller_avatar_url': seller_avatar_url,
                         },
                        status=status.HTTP_200_OK)
    except ReviewFreeAdSeller.DoesNotExist:
        return Response({'detail': 'Reviews not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @permission_classes([AllowAny])
def get_seller_paid_ad_reviews(request):

    ad_id = request.GET.get('ad_id', '')
    print("ad_id:", ad_id)

    ad = get_object_or_404(PostPaidAd, id=ad_id)
    seller = ad.seller

    try:
        seller_avatar = MarketplaceSellerPhoto.objects.get(seller=seller)
        seller_avatar_url = seller_avatar.photo.url
    except MarketplaceSellerPhoto.DoesNotExist:
        seller_avatar_url = None

    try:
        review_list = ReviewPaidAdSeller.objects.filter(
            paid_ad=ad).order_by('-timestamp')
        serializer = ReviewPaidAdSellerSerializer(review_list, many=True)
        return Response({'data': serializer.data,
                         'seller_avatar_url': seller_avatar_url,
                         },
                        status=status.HTTP_200_OK)
    except ReviewPaidAdSeller.DoesNotExist:
        return Response({'detail': 'Reviews not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def apply_promo_code(request):
    data = request.data

    promo_code = data.get('promo_code')
    ad_id = data.get('ad_id')
    selected_qty = data.get('selected_qty')
    print('ad_id:', ad_id, 'promo_code', promo_code, 'selected_qty', selected_qty)

    ad_promo = None

    try:
        ad_promo = PostPaidAd.objects.get(id=ad_id, promo_code=promo_code)
    except PostPaidAd.DoesNotExist:
        pass

    if not ad_promo:
        return Response({'detail': 'Invalid promo code or ad not found.'}, status=status.HTTP_400_BAD_REQUEST)

    # try:
    #     ad_promo = PostPaidAd.objects.get(id=ad_id, promo_code=promo_code)
    #     if not ad_promo:
    #         return Response({'detail': 'Invalid promo code.'}, status=status.HTTP_400_BAD_REQUEST)
    # except PostPaidAd.DoesNotExist:
    #     return Response({'detail': 'Invalid promo code or ad not found.'}, status=status.HTTP_400_BAD_REQUEST)

    promo_discount = 0
    discount_percentage = ad_promo.discount_percentage

    if discount_percentage:
        ad_price = ad_promo.price
        discount_amount = (discount_percentage / 100) * ad_price
        promo_discount = discount_amount.quantize(
            Decimal('0.00'), rounding=ROUND_DOWN) * selected_qty
        # promo_discount = promo_discount * selected_qty

    print('promo_discount:', promo_discount,
          'discount_percentage:', discount_percentage)

    return Response({'promo_discount': promo_discount, 'discount_percentage': discount_percentage}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def clear_seller_free_ad_message_counter(request):
    user = request.user
    data = request.data
    print('data:', data, 'user:', user)

    free_ad_message_id = data.get('free_ad_message_id')
    print('free_ad_message_id:', free_ad_message_id)

    try:
        ad_message_id = FreeAdMessageId.objects.get(
            free_ad_message_id=free_ad_message_id)
    except FreeAdMessageId.DoesNotExist:
        return Response({'detail': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)

    if ad_message_id.seller_free_ad_msg_count > 0:
        ad_message_id.seller_free_ad_msg_count = 0
        ad_message_id.save()
        print('seller_free_ad_msg_count (cleared):',
              ad_message_id.seller_free_ad_msg_count)

    return Response({'message': 'Message cleared.'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def clear_buyer_free_ad_message_counter(request):
    user = request.user
    data = request.data
    print('data:', data, 'user:', user)

    free_ad_message_id = data.get('free_ad_message_id')
    print('free_ad_message_id:', free_ad_message_id)

    try:
        ad_message_id = FreeAdMessageId.objects.get(
            free_ad_message_id=free_ad_message_id)
    except FreeAdMessageId.DoesNotExist:
        return Response({'detail': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)

    if ad_message_id.buyer_free_ad_msg_count > 0:
        ad_message_id.buyer_free_ad_msg_count = 0
        ad_message_id.save()
        print('buyer_msg_count (cleared):',
              ad_message_id.buyer_free_ad_msg_count)

    return Response({'message': 'Message cleared.'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def clear_seller_paid_ad_message_counter(request):
    user = request.user
    data = request.data
    print('data:', data, 'user:', user)

    paid_ad_message_id = data.get('paid_ad_message_id')
    print('paid_ad_message_id:', paid_ad_message_id)

    try:
        ad_message_id = PaidAdMessageId.objects.get(
            paid_ad_message_id=paid_ad_message_id)
    except PaidAdMessageId.DoesNotExist:
        return Response({'detail': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)

    if ad_message_id.seller_paid_ad_msg_count > 0:
        ad_message_id.seller_paid_ad_msg_count = 0
        ad_message_id.save()
        print('seller_paid_ad_msg_count (cleared):',
              ad_message_id.seller_paid_ad_msg_count)

    return Response({'message': 'Message cleared.'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def clear_buyer_paid_ad_message_counter(request):
    user = request.user
    data = request.data
    print('data:', data, 'user:', user)

    paid_ad_message_id = data.get('paid_ad_message_id')
    print('paid_ad_message_id:', paid_ad_message_id)

    try:
        ad_message_id = PaidAdMessageId.objects.get(
            paid_ad_message_id=paid_ad_message_id)
    except PaidAdMessageId.DoesNotExist:
        return Response({'detail': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)

    if ad_message_id.buyer_paid_ad_msg_count > 0:
        ad_message_id.buyer_paid_ad_msg_count = 0
        ad_message_id.save()
        print('buyer_msg_count (cleared):',
              ad_message_id.buyer_paid_ad_msg_count)

    return Response({'message': 'Message cleared.'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@permission_classes([IsAdminUser])
def get_all_sellers(request):
    try:
        sellers = User.objects.filter(is_marketplace_seller=True)
        serializer = UserSerializer(sellers, many=True)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response({'detail': 'Sellers not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@permission_classes([IsAdminUser])
def get_seller_account_detail(request, seller_username):
    seller = User.objects.get(username=seller_username) 
    print('seller_username:', seller_username)
    print('seller:', seller)
 
    try:
        seller_account_serializer = None
        seller_api_key_serializer = None
        seller_photo_url = None

        seller_account = MarketPlaceSellerAccount.objects.get(seller=seller)
        seller_account_serializer = MarketPlaceSellerAccountSerializer(seller_account)

        try:
            seller_api_key = PaysofterApiKey.objects.get(seller=seller)
            seller_api_key_serializer = PaysofterApiKeySerializer(seller_api_key)
        except PaysofterApiKey.DoesNotExist:
            seller_api_key_serializer = None
            pass
       
        try:
            seller_photo = MarketplaceSellerPhoto.objects.get(seller=seller)
            seller_photo_url = seller_photo.photo.url
        except MarketplaceSellerPhoto.DoesNotExist:
            seller_photo_url = None
            pass
        
        print('data processed!')
        return Response({
            'seller_account': seller_account_serializer.data if seller_account_serializer else None,
            'seller_api_key': seller_api_key_serializer.data if seller_api_key_serializer else None,
            'seller_photo_url': seller_photo_url,
        }, status=status.HTTP_200_OK)
    except MarketPlaceSellerAccount.DoesNotExist:
        return Response({'detail': 'Seller Account not found'}, status=status.HTTP_404_NOT_FOUND) 


@api_view(['POST'])
@permission_classes([IsAdminUser])
@permission_classes([IsAuthenticated])
def verify_seller(request):
    data = request.data
    admin_user = request.user
    print('data:', data)

    seller_username = data.get('seller_username')
    password = data.get('password')

    if not admin_user.check_password(password):
        return Response({'detail': 'Invalid password.'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        seller = User.objects.get(username=seller_username)
    except User.DoesNotExist:
        return Response({'detail': 'Seller fund not found.'}, status=status.HTTP_404_NOT_FOUND)

    seller.is_seller_account_verified = True
    seller.save()

    return Response({'detail': f'Success!', }, status=status.HTTP_200_OK) 


@api_view(['GET'])
@permission_classes([AllowAny])
def search_ads(request):

    search_term = request.GET.get('search_term', '')
    selected_country = request.GET.get('country', '')
    selected_state = request.GET.get('state', '')
    selected_city = request.GET.get('city', '')

    print('search_term:', search_term, 'location:',
          selected_country, selected_state, selected_city)

    try:
        search_term = search_term.strip()
        current_datetime = timezone.now()

        selected_country = request.GET.get('country', '')
        selected_state = request.GET.get('state', '')
        selected_city = request.GET.get('city', '')

        free_ads = PostFreeAd.objects.filter(
            Q(ad_name__icontains=search_term) |
            Q(description__icontains=search_term) |
            Q(brand__icontains=search_term),
            expiration_date__gt=current_datetime
        )

        paid_ads = PostPaidAd.objects.filter(
            Q(ad_name__icontains=search_term) |
            Q(description__icontains=search_term) |
            Q(brand__icontains=search_term),
            expiration_date__gt=current_datetime
        )

        if selected_country:
            free_ads = free_ads.filter(country=selected_country)
            paid_ads = paid_ads.filter(country=selected_country)

        if selected_state:
            free_ads = free_ads.filter(state_province=selected_state)
            paid_ads = paid_ads.filter(state_province=selected_state)

        if selected_city:
            free_ads = free_ads.filter(city=selected_city)
            paid_ads = paid_ads.filter(city=selected_city)

        free_ads_serializer = PostFreeAdSerializer(free_ads, many=True)
        paid_ads_serializer = PostPaidAdSerializer(paid_ads, many=True)

        if not free_ads.exists() and not paid_ads.exists():
            raise PostFreeAd.DoesNotExist

        return Response({
            'free_ads': free_ads_serializer.data,
            'paid_ads': paid_ads_serializer.data,
        }, status=status.HTTP_200_OK)

    except PostFreeAd.DoesNotExist:
        return Response({'detail': 'Ad not found in this location.'}, status=status.HTTP_404_NOT_FOUND)
    except PostPaidAd.DoesNotExist:
        return Response({'detail': 'Ad not found in this location.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @api_view(['GET'])
# @permission_classes([AllowAny])
# def search_ads(request, search_term):

#     try:
#         nltk.download('wordnet')

#         search_term = search_term.strip()
#         current_datetime = timezone.now()

#         synonyms = set()
#         for syn in wordnet.synsets(search_term):
#             for lemma in syn.lemmas():
#                 synonyms.add(lemma.name())

#         synonyms.add(search_term)

#         free_ads = PostFreeAd.objects.filter(
#             Q(ad_name__icontains=search_term) |
#             Q(description__icontains=search_term) |
#             Q(brand__icontains=search_term) |
#             Q(ad_name__icontains=synonyms) |
#             Q(description__icontains=synonyms) |
#             Q(brand__icontains=synonyms),
#             expiration_date__gt=current_datetime
#         )

#         paid_ads = PostPaidAd.objects.filter(
#             Q(ad_name__icontains=search_term) |
#             Q(description__icontains=search_term) |
#             Q(brand__icontains=search_term) |
#             Q(ad_name__icontains=synonyms) |
#             Q(description__icontains=synonyms) |
#             Q(brand__icontains=synonyms),
#             expiration_date__gt=current_datetime
#         )

#         free_ads_serializer = PostFreeAdSerializer(free_ads, many=True)
#         paid_ads_serializer = PostPaidAdSerializer(paid_ads, many=True)

#         if not free_ads.exists() and not paid_ads.exists():
#             raise PostFreeAd.DoesNotExist

#         return Response({
#             'free_ads': free_ads_serializer.data,
#             'paid_ads': paid_ads_serializer.data,
#         }, status=status.HTTP_200_OK)

#     except PostFreeAd.DoesNotExist:
#         return Response({'detail': 'Ad not found'}, status=status.HTTP_404_NOT_FOUND)
#     except PostPaidAd.DoesNotExist:
#         return Response({'detail': 'Ad not found'}, status=status.HTTP_404_NOT_FOUND)
#     except Exception as e:
#         return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PaymentDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        paystack_public_key = settings.PAYSTACK_PUBLIC_KEY
        paysofter_public_key = settings.PAYSOFTER_PUBLIC_KEY

        return Response({
            "paystackPublicKey": paystack_public_key,
            "paysofterPublicKey": paysofter_public_key,
        })
