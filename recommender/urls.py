from django.urls import path
from . import views

urlpatterns = [
    path('recommended-products/', views.get_recommended_products, name='recommended-products'),
]
