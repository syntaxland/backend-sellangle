# backend_drf/urls.py
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, 
    TokenVerifyView, 
)
# from live_chat import consumers

# websocket_urlpatterns = [
#     re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
# ]


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    
    path('api/', include('app.urls')),
    path('api/', include('user_profile.urls')),
    path('api/', include('send_email_otp.urls')), 
    path('api/', include('send_reset_password_email.urls')), 
    path('api/', include('payment.urls')),
    path('api/', include('credit_point.urls')),
    path('api/', include('send_email_message.urls')),
    path('api/', include('send_message_inbox.urls')),
    path('api/', include('recommender.urls')),
    path('api/', include('live_chat.urls')),
    path('', include('live_chat.urls')),
    path('api/', include('sellers.urls')),
    path('api/', include('marketplace.urls')),
    # path('api/', include('ecommerce.urls')),
    path('api/', include('promo.urls')),
    path('api/', include('support.urls')),
    path('api/', include('feedback.urls')),
] 

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
