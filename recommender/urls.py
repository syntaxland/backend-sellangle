from django.urls import path
from . import views

urlpatterns = [
    path('get-recommended-free-ads/', views.get_recommended_free_ads, name='get_recommended_free_ads'),
    path('get-recommended-paid-ads/', views.get_recommended_paid_ads, name='get_recommended_paid_ads'),
]
