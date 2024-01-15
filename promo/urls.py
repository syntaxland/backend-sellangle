from django.urls import path
from . import views

urlpatterns = [
    path("apply-promo-code/", views.apply_promo_code, name="apply-promo-code"),
    path("get-promo-discount/", views.apply_promo_code, name="get-promo-discount"),
    path('create-promo-code/', views.create_promo_code, name='create-promo-code'),
    path('promo-products/', views.get_valid_promo_products, name='promo-products'),
    
    path("generate-referral-link/", views.generate_referral_link, name="generate-referral-link"),
    path("generate-referral-link-button/", views.generate_referral_link_button, name="generate-referral-link-button"),
    path("get-user-referrals/", views.get_user_referrals, name="get-user-referrals"),
    path("get-all-referrals/", views.get_all_referrals, name="get-all-referrals"),
]
