from django.urls import path
from . import views

urlpatterns = [
    path('get-payment-details/', views.PaymentDetailsView.as_view(), name='get_payment_details'),
    path('create-payment/', views.create_payment, name='create_payment'),
    path('get-user-payments/', views.get_user_payments, name='get-user-payments'),
    path('get-all-payments/', views.get_all_payments_view, name='get-all-payments'),
]
