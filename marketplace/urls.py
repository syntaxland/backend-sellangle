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
    path('report-free-ad/', views.report_free_ad, name='report-free-ad'), 

    path('get-seller-paid-ad/', views.get_seller_paid_ad, name='get-seller-paid-ad'),
    path('get-seller-active-paid-ads/<str:seller_username>/', views.get_seller_active_paid_ads, name='get-seller-active-paid-ads'),
    path('get-paid-ad-detail/<int:pk>/', views.get_paid_ad_detail, name='get-paid-ad-detail'),
    path('edit-paid-ad/', views.update_seller_paid_ad, name='edit-paid-ad'),
    path('deactivate-paid-ad/', views.deactivate_paid_ad, name='delete-paid-ad'),
    path('reactivate-paid-ad/', views.reactivate_paid_ad, name='reactivate-paid-ad'),
    path('delete-paid-ad/', views.delete_paid_ad, name='delete-paid-ad'),
    path('get-all-paid-ad/', views.get_all_paid_ad, name='get-all-paid-ad'),
    path('report-paid-ad/', views.report_paid_ad, name='report-paid-ad'),

    path('get-seller-api-key/', views.get_seller_paysofter_api_key, name='get-seller-api-key'),
    path('save-seller-api-key/', views.save_seller_paysofter_api_key, name='save-seller-api-key'),

    path('create-free-ad-message/', views.create_free_ad_message, name='create-free-ad-message'),
    path('list-free-ad-messages/', views.list_free_ad_messages, name='list-free-ad-messages'),
    path('seller-reply-free-ad-message/', views.seller_reply_free_ad_message, name='seller_reply_free_ad_message'),
    path('list-seller-free-ad-messages/<int:pk>/', views.list_seller_free_ad_messages, name='list_seller_free_ad_messages'),
    path('get-buyer-free-ad-messages/', views.get_buyer_free_ad_messages, name='get_buyer_free_ad_messages'),

    path('create-paid-ad-message/', views.create_paid_ad_message, name='create-paid-ad-message'),
    path('list-paid-ad-messages/', views.list_paid_ad_messages, name='list-paid-ad-messages'),
    path('seller-reply-paid-ad-message/', views.seller_reply_paid_ad_message, name='seller_reply_paid_ad_message'),
    path('list-seller-paid-ad-messages/<int:pk>/', views.list_seller_paid_ad_messages, name='list_seller_paid_ad_messages'),
    path('get-buyer-paid-ad-messages/', views.get_buyer_paid_ad_messages, name='get_buyer_paid_ad_messages'),

    path('get-seller-shopfront-link/', views.get_seller_shopfront_link, name='get-seller-shopfront-link'),

    path('toggle-free-ad-save/', views.toggle_free_ad_save, name='toggle_free_ad_save'),
    path('toggle-paid-ad-save/', views.toggle_paid_ad_save, name='toggle_paid_ad_save'),
    path('track-free-ad-view/', views.track_free_ad_view, name='track_free_ad_view'),
    path('track-paid-ad-view/', views.track_paid_ad_view, name='track_paid_ad_view'),
    path('get-user-viewed-free-ads/', views.get_user_viewed_free_ads, name='get_user_viewed_free_ads'),
    path('get-user-viewed-paid-ads/', views.get_user_viewed_paid_ads, name='get_user_viewed_paid_ads'),
    path('get-user-saved-free-ads/', views.get_user_saved_free_ads, name='get_user_saved_free_ads'),
    path('get-user-saved-paid-ads/', views.get_user_saved_paid_ads, name='get_user_saved_paid_ads'),

    path('review-free-ad-seller/', views.review_free_ad_seller, name='review_free_ad_seller'),
    path('review-paid-ad-seller/', views.review_paid_ad_seller, name='review_paid_ad_seller'),

    path('get-seller-free-ad-reviews/', views.get_seller_free_ad_reviews, name='get_seller_free_ad_reviews'),
    path('get-seller-paid-ad-reviews/', views.get_seller_paid_ad_reviews, name='get_seller_paid_ad_reviews'),

    path('apply-promo-code/', views.apply_promo_code, name='apply_promo_code'),

    path('get-seller-paid-ads-charges/', views.get_seller_paid_ads_charges, name='get_seller_paid_ads_charges'),
    path('pay-ad-charges/', views.pay_ad_charges, name='pay_ad_charges'),
    path('get-ad-charges-receipt/', views.get_ad_charges_receipt, name='get_ad_charges_receipt'),
    
    # path('generate-ad-charges-receipt-pdf/', views.generate_ad_charges_receipt_pdf, name='generate_ad_charges_receipt_pdf'),
    # path('send-monthly-ad-billing-receipt-email/', views.send_monthly_ad_billing_receipt_email, name='send_monthly_ad_billing_receipt_email'),

    path('search-seller-username/<str:seller_username>/', views.search_seller_username, name='search-seller-username'),
    path('get-seller-detail/<str:seller_username>/', views.get_seller_detail, name='get-seller-detail'),

    path('search-ads/', views.search_ads, name='search-ads'),
]
