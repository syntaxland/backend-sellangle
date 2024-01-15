from django.urls import path
from . import views

urlpatterns = [
    path('password-reset-request/', views.send_password_reset_link_view, name='password_reset_request'),
    path('reset-password/<token>/', views.ResetPasswordView.as_view(), name='password_reset'),
]
