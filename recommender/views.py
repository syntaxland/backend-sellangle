from marketplace.models import (
                            PostFreeAd, 
                            PostPaidAd, 
                            )
from marketplace.serializers import (
                             PostFreeAdSerializer,
                             PostPaidAdSerializer, 
                            )

from rest_framework.decorators import api_view, permission_classes 
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Count, F, Q
from itertools import chain
from django.contrib.auth import get_user_model

User = get_user_model() 


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recommended_free_ads(request):
    user = request.user

    # Extract user preferences
    saved_ads = user.saved_free_ads.all()
    viewed_ads = user.viewed_free_ads.all()

    # Combine saved and viewed ads for user preferences
    user_ads = list(chain(saved_ads, viewed_ads))

    # Get ads with similar content based on user preferences
    similar_ads = PostFreeAd.objects.filter(
        Q(ad_category__in=[ad.ad_category for ad in user_ads]) |
        Q(ad_type__in=[ad.ad_type for ad in user_ads]) |
        Q(country__in=[ad.country for ad in user_ads]) |
        Q(description__in=[ad.description for ad in user_ads])
    ).exclude(id__in=[ad.id for ad in user_ads]).distinct()

    # Order similar ads by popularity
    similar_ads = similar_ads.annotate(
        popularity=Count('saved_free_ads') + Count('viewed_free_ads')
    ).order_by('-popularity')

    # Exclude user's own ads from recommendations
    similar_ads = similar_ads.exclude(seller=user)

    # Get the top N recommended ads
    N = 50  
    recommended_ads = similar_ads[:N]

    # Serialize the recommended ads
    serializer = PostFreeAdSerializer(recommended_ads, many=True)

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recommended_paid_ads(request):
    user = request.user

    # Extract user preferences
    saved_ads = user.saved_paid_ads.all()
    viewed_ads = user.viewed_paid_ads.all()

    # Combine saved and viewed ads for user preferences
    user_ads = list(chain(saved_ads, viewed_ads))

    # Get ads with similar content based on user preferences
    similar_ads = PostPaidAd.objects.filter(
        Q(ad_category__in=[ad.ad_category for ad in user_ads]) |
        Q(ad_type__in=[ad.ad_type for ad in user_ads]) |
        Q(country__in=[ad.country for ad in user_ads]) |
        Q(description__in=[ad.description for ad in user_ads])
    ).exclude(id__in=[ad.id for ad in user_ads]).distinct()

    # Order similar ads by popularity
    similar_ads = similar_ads.annotate(
        popularity=Count('saved_paid_ads') + Count('viewed_paid_ads')
    ).order_by('-popularity')

    # Exclude user's own ads from recommendations
    similar_ads = similar_ads.exclude(seller=user)

    # Get the top N recommended ads
    N = 50  
    recommended_ads = similar_ads[:N]

    # Serialize the recommended ads
    serializer = PostPaidAdSerializer(recommended_ads, many=True)

    return Response(serializer.data)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_recommended_free_ads(request):
#     user = request.user

#     saved_ads = user.saved_free_ads.all()
#     viewed_ads = user.viewed_free_ads.all()

#     saved_ad_name = saved_ads.values_list('ad_name', flat=True).distinct()
#     saved_ad_category = saved_ads.values_list('ad_category', flat=True).distinct()
#     saved_ad_type = saved_ads.values_list('ad_type', flat=True).distinct()
#     saved_country = saved_ads.values_list('country', flat=True).distinct()
#     saved_description = saved_ads.values_list('description', flat=True).distinct()

#     viewed_ad_name = viewed_ads.values_list('ad_name', flat=True).distinct()
#     viewed_ad_category = viewed_ads.values_list('ad_category', flat=True).distinct()
#     viewed_ad_type = viewed_ads.values_list('ad_type', flat=True).distinct()
#     viewed_country = viewed_ads.values_list('country', flat=True).distinct()
#     viewed_description = viewed_ads.values_list('description', flat=True).distinct()

#     recommended_free_ads = PostFreeAd.objects.filter(
#         Q(ad_name__in=saved_ad_name, 
#           ad_category__in=saved_ad_category, 
#           ad_type__in=saved_ad_type, 
#           country__in=saved_country, 
#           description__in=saved_description, 
#           ad_save_count__gt=0
#           )
#         | 
#         Q(ad_name__in=viewed_ad_name, 
#           ad_category__in=viewed_ad_category, 
#           ad_type__in=viewed_ad_type, 
#           country__in=viewed_country, 
#           description__in=viewed_description, 
#           ad_view_count__gt=0
#           )
#     ).exclude(user=user)

#     serializer = PostFreeAdSerializer(recommended_free_ads, many=True)

#     return Response(serializer.data)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_recommended_paid_ads(request):
#     user = request.user

#     saved_ads = user.saved_paid_ads.all()
#     viewed_ads = user.viewed_paid_ads.all()

#     saved_ad_name = saved_ads.values_list('ad_name', flat=True).distinct()
#     saved_ad_category = saved_ads.values_list('ad_category', flat=True).distinct()
#     saved_ad_type = saved_ads.values_list('ad_type', flat=True).distinct()
#     saved_country = saved_ads.values_list('country', flat=True).distinct()
#     saved_description = saved_ads.values_list('description', flat=True).distinct()

#     viewed_ad_name = viewed_ads.values_list('ad_name', flat=True).distinct()
#     viewed_ad_category = viewed_ads.values_list('ad_category', flat=True).distinct()
#     viewed_ad_type = viewed_ads.values_list('ad_type', flat=True).distinct()
#     viewed_country = viewed_ads.values_list('country', flat=True).distinct()
#     viewed_description = viewed_ads.values_list('description', flat=True).distinct()

#     recommended_paid_ads = PostPaidAd.objects.filter(
#         Q(ad_name__in=saved_ad_name, 
#           ad_category__in=saved_ad_category, 
#           ad_type__in=saved_ad_type, 
#           country__in=saved_country, 
#           description__in=saved_description, 
#           ad_save_count__gt=0
#           )
#         | 
#         Q(ad_name__in=viewed_ad_name, 
#           ad_category__in=viewed_ad_category, 
#           ad_type__in=viewed_ad_type, 
#           country__in=viewed_country, 
#           description__in=viewed_description, 
#           ad_view_count__gt=0
#           )
#     ).exclude(user=user)

#     serializer = PostPaidAdSerializer(recommended_paid_ads, many=True)

#     return Response(serializer.data)




