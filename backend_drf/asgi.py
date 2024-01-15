# backend_drf/asgi.py

"""
ASGI config for backend_drf project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import live_chat.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_drf.settings')

application = ProtocolTypeRouter({
    'http':get_asgi_application(),
    'websocket':AuthMiddlewareStack(
        URLRouter(
            live_chat.routing.websocket_urlpatterns
        )
    )
})


# import os

# from django.core.asgi import get_asgi_application
# # from channels.routing import get_default_application
# from channels.routing import ProtocolTypeRouter


# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_drf.settings')

# # application = get_asgi_application()
# # application = get_default_application()
# application = ProtocolTypeRouter({
#     'http':get_asgi_application()
# })
