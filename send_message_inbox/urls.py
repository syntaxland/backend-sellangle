from django.urls import path
from . import views

urlpatterns = [
    path('send-message-to-all/', views.send_message_to_all, name='send-message-to-all'),
    path('message-inbox/', views.message_inbox_view, name='message-inbox'),
]
 