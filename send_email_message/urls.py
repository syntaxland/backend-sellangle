from django.urls import path
from . import views

urlpatterns = [
    path('send-email-to-all/', views.send_email_to_all_users, name='send_email_message'),
]
