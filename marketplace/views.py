# marketplace/views.py 
from decimal import ROUND_DOWN, Decimal
from datetime import datetime, timedelta, timezone

from django.shortcuts import get_object_or_404

import nltk
from nltk.corpus import wordnet
 
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from credit_point.models import CreditPoint
from .models import (MarketPlaceSellerAccount, 
                     MarketplaceSellerPhoto, 
                     PostFreeAd, PostPaidAd, 
                     PaysofterApiKey, Message,
                    ReportFreeAd, ReportPaidAd, 
                    ReviewFreeAdSeller, ReviewPaidAdSeller

                     )
from .serializers import (MarketPlaceSellerAccountSerializer,
                           MarketplaceSellerPhotoSerializer,
                             PostFreeAdSerializer, PostPaidAdSerializer, 
                             PaysofterApiKeySerializer, MessageSerializer,
                             ReportFreeAdSerializer, ReportPaidAdSerializer,
                            ReviewFreeAdSellerSerializer, ReviewPaidAdSellerSerializer
                            )
from user_profile.serializers import UserSerializer

from django.conf import settings
from django.db.models import Avg
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()

 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def create_marketplace_seller(request):
    data=request.data
    print('data:', data)

    seller, created = MarketPlaceSellerAccount.objects.get_or_create(seller=request.user)
    serializer = MarketPlaceSellerAccountSerializer(instance=seller, data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def create_marketplace_seller_photo(request):
    seller=request.user
    data=request.data
    print('seller:', seller)
    print('data:', data)
    photo, created = MarketplaceSellerPhoto.objects.get_or_create(seller=seller)
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
        if free_ad_count >= 3:
            return Response({'detail': f'You can only post a maximum of 3 free ads. You have posted {free_ad_count} free ads.'}, status=status.HTTP_400_BAD_REQUEST) 
    except User.DoesNotExist:
        pass

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

            ad.duration_hours = durations_mapping.get(ad.duration, timedelta(hours=0))
            ad.expiration_date = datetime.now() + ad.duration_hours

        ad.is_active = True
        ad.save()

        return Response({'success': f'Ad created successfully.'}, status=status.HTTP_201_CREATED)
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
        if credit_point_balance < 24:
            return Response({'detail': f'Your credit point credit point balance of {credit_point_balance} is too low. You need at least 24 cps to place a paid ad.'}, 
                            status=status.HTTP_400_BAD_REQUEST)
    except CreditPoint.DoesNotExist:
        pass

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

            ad.duration_hours = durations_mapping.get(ad.duration, timedelta(hours=0))
            ad.expiration_date = datetime.now() + ad.duration_hours

        ad.is_active = True
        ad.save()

        return Response({'success': f'Ad created successfully.'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# @parser_classes([MultiPartParser, FormParser])
# def create_paid_ad(request):
#     seller = request.user
#     data = request.data
#     serializer = PostPaidAdSerializer(data=data)

#     try:
#         credit_point = CreditPoint.objects.get(user=seller)
#         credit_point_balance = credit_point.balance
#         print('credit_point_balance:', credit_point_balance)

#         if serializer.is_valid():
#             ad_duration = serializer.validated_data.get('duration', None)
#             print('ad_duration:', ad_duration)

#             if ad_duration:
#                 durations_mapping = {
#                     '1 day': 24,
#                     '2 days': 48,
#                     '3 days': 72,
#                     '5 days': 120,
#                     '1 week': 180,
#                     '2 weeks': 360,
#                     '1 month': 720,
#                 }

#                 required_cps = durations_mapping.get(ad_duration, 0)

#                 if credit_point_balance < required_cps:
#                     return Response({
#                         'detail': f'Your credit point balance of {credit_point_balance} is too low. You need at least {required_cps} cps to place a paid ad for {ad_duration}.'
#                     }, status=status.HTTP_400_BAD_REQUEST)

#             ad = serializer.save(seller=seller)

#             if ad_duration:
#                 ad_duration_hours = timedelta(hours=durations_mapping.get(ad_duration, 0))
#                 ad.expiration_date = datetime.now() + ad_duration_hours
#                 ad.is_active = True
#                 ad.save()

#                 return Response({'success': f'Ad created successfully.'}, status=status.HTTP_201_CREATED)

#     except User.DoesNotExist:
#         pass

#     return Response({'detail': 'Error processing the request.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def get_marketplace_seller_account(request):
    user = request.user
    try:
        marketplace_seller_account = MarketPlaceSellerAccount.objects.get(seller=user)
        serializer = MarketPlaceSellerAccountSerializer(marketplace_seller_account)
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
        marketplace_seller_account = MarketPlaceSellerAccount.objects.get(seller=user)
    except MarketPlaceSellerAccount.DoesNotExist:
        return Response({'detail': 'Marketplace seller account not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = MarketPlaceSellerAccountSerializer(marketplace_seller_account, data, partial=True)
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
        marketplace_seller_photo = MarketplaceSellerPhoto.objects.get(seller=user)
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
        marketplace_seller_photo = MarketplaceSellerPhoto.objects.get(seller=user)
    except MarketplaceSellerPhoto.DoesNotExist:
        return Response({'detail': 'Marketplace seller photo not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = MarketplaceSellerPhotoSerializer(marketplace_seller_photo, data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'detail': 'Marketplace seller photo updated successfully.'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def get_seller_free_ad(request):
    user = request.user
    # current_datetime = datetime.now()
    try:
        free_ad = PostFreeAd.objects.filter(seller=user) 
        # free_ad = PostFreeAd.objects.filter(seller=user, expiration_date__gt=current_datetime)
        serializer = PostFreeAdSerializer(free_ad, many=True)
        return Response(serializer.data)
    except PostFreeAd.DoesNotExist:
        return Response({'detail': 'Free ad not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def get_seller_active_free_ads(request, seller_username):
    seller = User.objects.get(username=seller_username)
    print('seller_username:', seller_username)

    current_datetime = datetime.now()

    try:
        free_ad = PostFreeAd.objects.filter(seller=seller, expiration_date__gt=current_datetime)
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
            # return Response({'detail': 'MarketplaceSellerPhoto not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            seller_info = MarketPlaceSellerAccount.objects.get(seller=seller)
            is_seller_verified = seller_info.is_seller_verified
        except MarketPlaceSellerAccount.DoesNotExist:
            is_seller_verified = None

        # serializer = PostPaidAdSerializer(ad, context={'seller_avatar_url': seller_avatar_url})

        serializer = PostFreeAdSerializer(ad)
        return Response({'data': serializer.data, 
                         'sellerApiKey': seller_api_key,
                          'seller_avatar_url': seller_avatar_url,
                          'is_seller_verified': is_seller_verified,
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

            ad.duration_hours = durations_mapping.get(ad.duration, timedelta(hours=0))
            ad.expiration_date = datetime.now() + ad.duration_hours

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

            ad.duration_hours = durations_mapping.get(ad.duration, timedelta(hours=0))
            ad.expiration_date = datetime.now() + ad.duration_hours

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

    current_datetime = datetime.now()

    selected_country = request.GET.get('country', '')
    selected_state = request.GET.get('state', '')
    selected_city = request.GET.get('city', '')
    # selected_category = request.GET.get('category', '') 
    # selected_type = request.GET.get('type', '')
    print('free location:', selected_country, selected_state, selected_city)

    try:
        free_ads = PostFreeAd.objects.filter(expiration_date__gt=current_datetime).order_by("?")

        if selected_country:
            free_ads = free_ads.filter(country=selected_country)
        if selected_state:
            free_ads = free_ads.filter(state_province=selected_state)
        if selected_city:
            free_ads = free_ads.filter(city=selected_city)
        # if selected_category:
        #     free_ads = free_ads.filter(ad_category=selected_category)
        # if selected_type:
        #     free_ads = free_ads.filter(ad_type=selected_type)

        serializer = PostFreeAdSerializer(free_ads, many=True)
        return Response(serializer.data)
    except PostFreeAd.DoesNotExist:
        return Response({'detail': 'Free ad not found'}, status=status.HTTP_404_NOT_FOUND)

        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def get_seller_paid_ad(request):
    user = request.user
    # current_datetime = datetime.now()
    try:
        paid_ad = PostPaidAd.objects.filter(seller=user)
        # paid_ad = PostPaidAd.objects.filter(seller=user, expiration_date__gt=current_datetime)
        serializer = PostPaidAdSerializer(paid_ad, many=True)
        return Response(serializer.data)
    except PostPaidAd.DoesNotExist:
        return Response({'detail': 'Paid ad not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def get_seller_active_paid_ads(request, seller_username):
    seller = User.objects.get(username=seller_username)
    print('seller_username:', seller_username)

    current_datetime = datetime.now()
    try:
        paid_ad = PostPaidAd.objects.filter(seller=seller, expiration_date__gt=current_datetime)
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
            # return Response({'detail': 'PaysofterApiKey not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            seller_avatar = MarketplaceSellerPhoto.objects.get(seller=seller)
            seller_avatar_url = seller_avatar.photo.url
        except MarketplaceSellerPhoto.DoesNotExist:
            seller_avatar_url = None
            # return Response({'detail': 'MarketplaceSellerPhoto not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            seller_info = MarketPlaceSellerAccount.objects.get(seller=seller)
            is_seller_verified = seller_info.is_seller_verified
        except MarketPlaceSellerAccount.DoesNotExist:
            is_seller_verified = None
            

        serializer = PostPaidAdSerializer(ad, context={'seller_avatar_url': seller_avatar_url})

        return Response({'data': serializer.data, 
                         'sellerApiKey': seller_api_key, 
                         'seller_avatar_url': seller_avatar_url,
                        'is_seller_verified': is_seller_verified,
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
        if credit_point_balance < 24:
            return Response({'detail': f'Your credit point credit point balance of {credit_point_balance} is too low. You need at least 24 cps to complete this action.'}, 
                            status=status.HTTP_400_BAD_REQUEST)
    except CreditPoint.DoesNotExist:
        pass

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

            ad.duration_hours = durations_mapping.get(ad.duration, timedelta(hours=0))
            ad.expiration_date = datetime.now() + ad.duration_hours

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
        if credit_point_balance < 24:
            return Response({'detail': f'Your credit point credit point balance of {credit_point_balance} is too low. You need at least 24 cps to complete this action.'}, 
                            status=status.HTTP_400_BAD_REQUEST)
    except CreditPoint.DoesNotExist:
        pass
    
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

            ad.duration_hours = durations_mapping.get(ad.duration, timedelta(hours=0))
            ad.expiration_date = datetime.now() + ad.duration_hours

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

    current_datetime = datetime.now()

    selected_country = request.GET.get('country', '')
    selected_state = request.GET.get('state', '')
    selected_city = request.GET.get('city', '')

    # selected_category = request.GET.get('category', '')  
    # selected_type = request.GET.get('type', '')
    print('paid location:', selected_country, selected_state, selected_city)

    try:
        paid_ads = PostPaidAd.objects.filter(expiration_date__gt=current_datetime).order_by("?")

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


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def save_seller_paysofter_api_key(request):
    user = request.user
    data = request.data
    print('data:', data)

    api_key, created = PaysofterApiKey.objects.get_or_create(seller=request.user)
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
def create_free_ad_message(request):
    user=request.user
    data=request.data
    print('data:', data, 'user:', user)

    pk = data.get('pk')
    message = data.get('message')
    print('pk:', pk)
    print('message:', message)
    
    try:
        free_ad = PostFreeAd.objects.get(pk=pk)
    except PostFreeAd.DoesNotExist:
        return Response({'detail': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)
    
    Message.objects.create(
            user=user,
            message=message,
            free_ad=free_ad,
        )
    return Response({'message': 'Message created'}, status=status.HTTP_201_CREATED)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_free_ad_messages(request, pk):
    user = request.user
    print('user:', user)

    try:
        free_ad = PostFreeAd.objects.get(pk=pk)
    except PostFreeAd.DoesNotExist:
        return Response({'detail': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)
    
    print('free_ad:', free_ad)
    
    try:
        ad_message = Message.objects.filter(
            # user=user,
            free_ad=free_ad,
            ).order_by('timestamp')
        serializer = MessageSerializer(ad_message, many=True) 
        return Response(serializer.data)
    except Message.DoesNotExist:
        return Response({'detail': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def seller_reply_free_ad_message(request):
    seller=request.user
    data=request.data
    print('data:', data)

    pk = data.get('pk')
    message = data.get('message')
    print('pk:', pk)
    print('message:', message)
    
    try:
        free_ad = PostFreeAd.objects.get(pk=pk)
    except PostFreeAd.DoesNotExist:
        return Response({'detail': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)
    
    Message.objects.create(
            seller=seller,
            message=message,
            free_ad=free_ad,
        )
    return Response({'message': 'Message created'}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_seller_free_ad_messages(request, pk):
    seller = request.user
    # data  = request.data
    # print('data:', data)
    print('seller:', seller)

    try:
        free_ad = PostFreeAd.objects.get(pk=pk)
    except PostFreeAd.DoesNotExist:
        return Response({'detail': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)
    
    print('free_ad:', free_ad)
    
    try:
        ad_message = Message.objects.filter(
            seller=seller,
            free_ad=free_ad,
            ).order_by('timestamp')
        serializer = MessageSerializer(ad_message, many=True) 
        return Response(serializer.data)
    except Message.DoesNotExist:
        return Response({'detail': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_paid_ad_message(request):
    user=request.user
    data=request.data
    print('data:', data, 'user:', user)

    pk = data.get('pk')
    message = data.get('message')
    print('pk:', pk)
    print('message:', message)
    
    try:
        paid_ad = PostPaidAd.objects.get(pk=pk)
    except PostPaidAd.DoesNotExist:
        return Response({'detail': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)
    
    Message.objects.create(
            user=user,
            message=message,
            paid_ad=paid_ad,
        )
    return Response({'message': 'Message created'}, status=status.HTTP_201_CREATED)
 

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_paid_ad_messages(request, pk):
    user = request.user
    # data  = request.data
    # print('data:', data)
    print('user:', user)

    try:
        paid_ad = PostPaidAd.objects.get(pk=pk)
    except PostPaidAd.DoesNotExist:
        return Response({'detail': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)
    
    print('paid_ad:', paid_ad)
    
    try:
        ad_message = Message.objects.filter(
            # user=user,
            paid_ad=paid_ad,
            ).order_by('timestamp')
        serializer = MessageSerializer(ad_message, many=True) 
        return Response(serializer.data)
    except Message.DoesNotExist:
        return Response({'detail': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_buyer_free_ad_messages(request):
    user = request.user
    print('user:', user)

    current_datetime = datetime.now()
    seller_free_ads = PostFreeAd.objects.filter(seller=user, expiration_date__gt=current_datetime)
    messages = Message.objects.filter(free_ad__in=seller_free_ads).order_by('-timestamp')
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_buyer_paid_ad_messages(request):
    user = request.user
    print('user:', user)

    current_datetime = datetime.now()
    seller_paid_ads = PostPaidAd.objects.filter(seller=user, expiration_date__gt=current_datetime)
    messages = Message.objects.filter(paid_ad__in=seller_paid_ads).order_by('-timestamp')
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_buyer_paid_ad_messages(request, pk):
#     seller = request.user
#     # data  = request.data
#     # print('data:', data)
#     print('seller:', seller)

#     try:
#         paid_ad = PostPaidAd.objects.filter(seller=seller)
#     except PostPaidAd.DoesNotExist:
#         return Response({'detail': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)
    
#     print('paid_ad:', paid_ad)
    
#     try:
#         ad_message = Message.objects.filter(
#             # seller=seller,
#             paid_ad=paid_ad,
#             ).order_by('timestamp')
#         serializer = MessageSerializer(ad_message, many=True) 
#         return Response(serializer.data)
#     except Message.DoesNotExist:
#         return Response({'detail': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def seller_reply_paid_ad_message(request):
    seller=request.user
    data=request.data
    print('data:', data, 'seller:', seller)

    pk = data.get('pk')
    message = data.get('message')
    print('pk:', pk)
    print('message:', message)
    
    try:
        paid_ad = PostPaidAd.objects.get(pk=pk)
    except PostPaidAd.DoesNotExist:
        return Response({'detail': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)
    
    Message.objects.create(
            seller=seller,
            message=message,
            paid_ad=paid_ad,
        )
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
    
    print('paid_ad:', paid_ad)
    
    try:
        ad_message = Message.objects.filter(
            seller=seller,
            paid_ad=paid_ad,
            ).order_by('timestamp')
        serializer = MessageSerializer(ad_message, many=True) 
        return Response(serializer.data)
    except Message.DoesNotExist:
        return Response({'detail': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
@permission_classes([AllowAny])
def search_seller_username(request, seller_username):

    try:
        seller = User.objects.get(username=seller_username, is_marketplace_seller=True)
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
    url = settings.MCDOFSHOP_URL
    print("url:", url)
    print("user:", user)

    try:
        shopfront_link =  f"{url}/seller-shop-front/{user.username}/"
        print("shopfront_link:", shopfront_link)
        return Response({"shopfrontLink": shopfront_link}, status=status.HTTP_200_OK)
    except object.DoesNotExist:
        return Response({'detail': 'Link not found'}, status=status.HTTP_404_NOT_FOUND)
    # except Exception as e:
    #     return Response( {"error": str(e)},  status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def get_seller_detail(request, seller_username):

    seller = User.objects.get(username=seller_username)

    try:
        seller_avatar = MarketplaceSellerPhoto.objects.get(seller=seller)
        seller_avatar_url = seller_avatar.photo.url
    except MarketplaceSellerPhoto.DoesNotExist:
        seller_avatar_url = None

    try:
        seller_detail = MarketPlaceSellerAccount.objects.get(seller=seller)
        serializer = MarketPlaceSellerAccountSerializer(seller_detail)

        return Response({'data': serializer.data, 'seller_avatar_url': seller_avatar_url}, status=status.HTTP_200_OK)
    
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

    if request.method == 'POST':
        ad_id = request.data.get('ad_id')
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

    if request.method == 'POST':
        ad_id = request.data.get('ad_id')
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
    try:
        viewed_ads = user.viewed_free_ads.all()
        serializer = PostFreeAd(viewed_ads, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_viewed_paid_ads(request):
    user = request.user
    try:
        viewed_ads = user.viewed_paid_ads.all()
        serializer = PostPaidAd(viewed_ads, many=True)
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
    if request.method == 'POST':
        order_item_id = request.data.get('order_item_id')
        rating = request.data.get('rating')
        comment = request.data.get('comment')
        print(order_item_id, rating, comment)

        order_item = get_object_or_404(PostFreeAd, _id=order_item_id)

        if user == order_item.order.user: 
            review = ReviewFreeAdSeller.objects.create(
                order_item=order_item,
                rating=rating,
                comment=comment,
                user=user,
                product=order_item.product,
                name=order_item.name, 
            )

            
            product = order_item.product
            reviews = ReviewFreeAdSeller.objects.filter(product=product)
            product.numReviews = reviews.count()
            product.rating = reviews.aggregate(Avg('rating'))['rating__avg']
            product.save()
            
            serializer = ReviewFreeAdSellerSerializer(review, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': 'You are not authorized to add a review for this order item.'}, 
                            status=status.HTTP_403_FORBIDDEN)
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
# @permission_classes([IsAuthenticated])
def review_free_ad_list(request, product_id):
    print('product_id:',product_id)
    try:
        review_list = ReviewFreeAdSeller.objects.filter(product_id=product_id).order_by('-createdAt')
        serializer = ReviewFreeAdSellerSerializer(review_list, many=True)
        return Response(serializer.data)
    except ReviewFreeAdSeller.DoesNotExist:
        return Response({'detail': 'Reviews not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_seller_free_ad_reviews(request):
    user = request.user
    try:
        order_reviews = ReviewFreeAdSeller.objects.filter(user=user).order_by('-createdAt')
        serializer = ReviewFreeAdSellerSerializer(order_reviews, many=True)
        return Response(serializer.data)
    except ReviewFreeAdSeller.DoesNotExist:
        return Response({'detail': 'Reviews not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated]) 
def apply_paid_ad_promo_code(request):
    data = request.data
    promo_code = data.get('promoCode')
    ad_id = data.get('ad_id')
    print('promo_code, ad_id:', promo_code, ad_id)

    try:
        ad_promo = PostPaidAd.objects.get(id=ad_id, promo_code=promo_code)
    except PostPaidAd.DoesNotExist:
        return Response({'detail': 'Invalid promo code or ad not found.'}, status=status.HTTP_400_BAD_REQUEST)

    promo_discount = 0
    discount_percentage = ad_promo.discount_percentage

    if discount_percentage:
        ad_price = ad_promo.price
        discount_amount = (discount_percentage / 100) * ad_price
        promo_discount = discount_amount.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

    print('apply_promo_code promo_discount:', promo_discount, 'discount_percentage:', discount_percentage)

    return Response({'promoDiscount': promo_discount, 'discountPercentage': discount_percentage}, status=status.HTTP_200_OK)
    

# @api_view(['GET'])
# @permission_classes([AllowAny])
# def search_ads(request, search_term):

#     try:
#         search_term = search_term.strip()
#         current_datetime = datetime.now()

#         free_ads = PostFreeAd.objects.filter(
#             Q(ad_name__icontains=search_term) |
#             Q(description__icontains=search_term) |
#             Q(brand__icontains=search_term),
#             expiration_date__gt=current_datetime
#         )

#         paid_ads = PostPaidAd.objects.filter(
#             Q(ad_name__icontains=search_term) |
#             Q(description__icontains=search_term) |
#             Q(brand__icontains=search_term),
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


@api_view(['GET'])
@permission_classes([AllowAny])
def search_ads(request):

    search_term = request.GET.get('search_term', '')
    selected_country = request.GET.get('country', '')
    selected_state = request.GET.get('state', '')
    selected_city = request.GET.get('city', '')

    print('search_term:', search_term, 'location:', selected_country, selected_state, selected_city)

    try:
        search_term = search_term.strip()
        current_datetime = datetime.now()

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
#         current_datetime = datetime.now()

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


