# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create-marketplace-seller/', views.create_marketplace_seller, name='create-marketplace-seller'),
    path('marketplace-seller-photo/', views.create_marketplace_seller_photo, name='marketplace-seller-photo'),

    path('create-free-ad/', views.create_free_ad, name='create-free-ad'),
    path('create-paid-ad/', views.create_paid_ad, name='create-paid-ad'),

    path('get-marketplace-seller-account/', views.get_marketplace_seller_account, name='get-marketplace-seller-account'),
    path('update-marketplace-seller-account/', views.update_marketplace_seller_account, name='update-marketplace-seller-account'),

    path('get-marketplace-seller-photo/', views.get_marketplace_seller_photo, name='get_marketplace-seller-photo'),
    path('update-marketplace-seller-photo/', views.update_marketplace_seller_photo, name='update-marketplace-seller-photo'),

    path('get-seller-free-ad/', views.get_seller_free_ad, name='get-seller-free-ad'),
    path('get-seller-active-free-ads/<str:seller_username>/', views.get_seller_active_free_ads, name='get-seller-active-free-ads'),
    path('get-free-ad-detail/<int:pk>/', views.get_free_ad_detail, name='get-free-ad-detail'),

    path('edit-free-ad/', views.update_seller_free_ad, name='edit-free-ad'),
    path('deactivate-free-ad/', views.deactivate_free_ad, name='delete-free-ad'),
    path('reactivate-free-ad/', views.reactivate_free_ad, name='reactivate-free-ad'),
    path('delete-free-ad/', views.delete_free_ad, name='delete-free-ad'),
    path('get-all-free-ad/', views.get_all_free_ad, name='get-all-free-ad'),

    path('get-seller-paid-ad/', views.get_seller_paid_ad, name='get-seller-paid-ad'),
    path('get-seller-active-paid-ads/<str:seller_username>/', views.get_seller_active_paid_ads, name='get-seller-active-paid-ads'),
    path('get-paid-ad-detail/<int:pk>/', views.get_paid_ad_detail, name='get-paid-ad-detail'),
    path('edit-paid-ad/', views.update_seller_paid_ad, name='edit-paid-ad'),
    path('deactivate-paid-ad/', views.deactivate_paid_ad, name='delete-paid-ad'),
    path('reactivate-paid-ad/', views.reactivate_paid_ad, name='reactivate-paid-ad'),
    path('delete-paid-ad/', views.delete_paid_ad, name='delete-paid-ad'),
    path('get-all-paid-ad/', views.get_all_paid_ad, name='get-all-paid-ad'),

    path('get-seller-api-key/', views.get_seller_paysofter_api_key, name='get-seller-api-key'),
    path('save-seller-api-key/', views.save_seller_paysofter_api_key, name='save-seller-api-key'),

    path('create-paid-ad-message/', views.create_paid_ad_message, name='create-paid-ad-message'),
    path('list-paid-ad-messages/<int:pk>/', views.list_paid_ad_messages, name='list-paid-ad-messages'),

    path('create-free-ad-message/', views.create_free_ad_message, name='create-free-ad-message'),
    path('list-free-ad-messages/<int:pk>/', views.list_free_ad_messages, name='list-free-ad-messages'),

    path('get-seller-shopfront-link/', views.get_seller_shopfront_link, name='get-seller-shopfront-link'),

    path('search-seller-username/<str:seller_username>/', views.search_seller_username, name='search-seller-username'),
    path('get-seller-detail/<str:seller_username>/', views.get_seller_detail, name='get-seller-detail'),

    path('search-ads/', views.search_ads, name='search-ads'),
]
