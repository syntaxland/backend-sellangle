from django.db.models import Count, F, Q
from django.db.models.functions import Coalesce
from django.db.models import Value
from django.db.models import CharField
from app.models import Product
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from app.serializer import ProductSerializer
from django.contrib.auth import get_user_model

User = get_user_model() 


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recommended_products(request):
    user = request.user

    # Get user's saved products
    saved_products = user.favorite_products.all()

    # Get user's viewed products
    viewed_products = user.viewed_products.all()

    # Extract the brands and categories of saved and viewed products
    saved_brands = saved_products.values_list('brand', flat=True).distinct()
    saved_categories = saved_products.values_list('category', flat=True).distinct()

    viewed_brands = viewed_products.values_list('brand', flat=True).distinct()
    viewed_categories = viewed_products.values_list('category', flat=True).distinct()

    # Combine saved and viewed products
    recommended_products = Product.objects.filter(
        Q(brand__in=saved_brands, category__in=saved_categories, save_count__gt=0)
        | Q(brand__in=viewed_brands, category__in=viewed_categories, view_count__gt=0)
    ).exclude(user=user)

    # Serialize the recommended products
    serializer = ProductSerializer(recommended_products, many=True)

    return Response(serializer.data)


# # views.py
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import UserInteraction
# from app.models import Product
# from app.serializer import ProductSerializer

# class ProductRecommendations(APIView):
#     def get(self, request):
#         user = request.user  # Assuming you're using authentication
#         # Get user's saved and viewed products
#         saved_products = UserInteraction.objects.filter(
#             user=user, interaction_type='save'
#         ).values_list('product', flat=True)
#         viewed_products = UserInteraction.objects.filter(
#             user=user, interaction_type='view'
#         ).values_list('product', flat=True)
#         # Combine and remove duplicates
#         user_interactions = set(saved_products) | set(viewed_products)
#         # Generate recommendations (e.g., 5 products)
#         recommendations = Product.objects.exclude(id__in=user_interactions)[:5]
#         # Serialize recommendations and return
#         serializer = ProductSerializer(recommendations, many=True)
#         return Response(serializer.data)
