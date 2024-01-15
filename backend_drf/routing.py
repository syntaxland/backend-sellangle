# backend_drf/routing.py
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path, include
import live_chat.routing

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            live_chat.routing.websocket_urlpatterns  
        )
    ),
})


# websocket_urlpatterns = [
#     path('ws/chat/', include('live_chat.routing.websocket_urlpatterns')),
# ]

# application = ProtocolTypeRouter({
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             websocket_urlpatterns
#         )
#     ),
# })
