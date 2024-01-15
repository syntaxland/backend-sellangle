from django.urls import path
from . import views

urlpatterns = [
    path('users/register/', views.register_user_view, name='user-register'),
    path('users/login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('google-login/', views.GoogleLogin.as_view(), name='google_login'),
    path('users/logout/', views.LogoutView.as_view(), name='user-logout'),
    path('get-user-profile/', views.GetUserProfileView.as_view(), name='get_user_profile'),
    path('update-user-profile/', views.UpdateUserProfileView.as_view(), name='update_user_profile'),
    path('users/update-avatar/', views.UpdateUserAvatarView.as_view(), name='update_user_avatar'),
    path('change-password/', views.change_password_view, name='change_password_view'),
    path('user-account-delete/', views.AccountDeleteView.as_view(), name='user-account-delete'),

    # path('toggle-favorite/<int:product_id>/', views.toggle_favorite),
]
