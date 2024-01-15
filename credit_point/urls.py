from django.urls import path
from . import views

urlpatterns = [
    path('credit-point-request/', views.credit_point_request_view, name='credit_point_request'),
    path('get-all-credit-point-requests/', views.get_all_credit_points_request_view, name='get-all-credit-points'),
    path('get-credit-point/', views.get_user_credit_point_request_view, name='get-credit-point'),
    path('get-credit-point-balance/', views.get_credit_points_balance_view, name='get-credit-point-balance'),
    path('get-user-credit-point-earnings/', views.get_user_credit_point_earnings, name='get-user-credit-point-earnings'),

    # path('get-user-credit-point-payments/', views.get_user_credit_point_payments, name='get-user-credit-point-payments'),
    # path('get-all-credit-point-payments/', views.get_all_credit_point_payments, name='get-all-credit-point-payments'),
    # path('get-all-credit-point-payments/', views.get_all_credit_point_payments, name='get-all-credit-point-payments'),

    path('sell-credit-point/', views.sell_credit_point, name='sell-credit-point'),
    path('get-user-buy-credit-point/', views.get_user_buy_credit_point, name='get-user-buy-credit-point'),

    path('buy-credit-point/', views.buy_credit_point, name='buy-credit-point'), 
    path('get-user-sell-credit-point/', views.get_seller_credit_point, name='get-user-sell-credit-point'),
    path('get-buyer-credit-point/', views.get_buyer_credit_point, name='get-buyer-credit-point'),

]
