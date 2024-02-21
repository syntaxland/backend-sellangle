from django.urls import path
from . import views

urlpatterns = [
    path('send-message-to-all/', views.send_message_to_all, name='send-message-to-all'),
    path('message-inbox/', views.message_inbox_view, name='message-inbox'),
    path('clear-message-counter/', views.clear_message_counter, name='clear-message-counter'),
    path('get-user-message-inbox/', views.get_user_message_inbox, name='get_user_message_inbox'),
]
 