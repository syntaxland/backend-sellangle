# live_chat/urls.py
from django.urls import path, re_path
from . import consumers
from . import views

urlpatterns = [
    path('live-chat/', views.live_chat, name='live-chat'),

    path('chat-rooms/', views.ChatRoomListView.as_view(), name='chat-room-list'),
    path('chat-messages/<str:room_name>/', views.create_chat_message, name='chat-message-list'),
    # path('chat-messages/<str:room_name>/', views.ChatMessageListView.as_view(), name='chat-message-list'),
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]
