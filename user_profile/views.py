# user_profile/views.py
import random
import string
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status, generics
from rest_framework.request import Request
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView 

from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.oauth2.views import OAuth2Adapter
# from allauth.socialaccount.providers.oauth2.views import SocialLoginView
from rest_auth.registration.serializers import SocialLoginSerializer

# from .models import UserProfile
from .serializers import (
    UserSerializer,
    UserSerializerWithToken,
    MyTokenObtainPairSerializer,
    DeleteAccountSerializer, 
    ChangePasswordSerializer,
    UpdateUserProfileSerializer,
    AvatarUpdateSerializer,
    GoogleLoginSerializer
)

from send_email_otp.serializers import EmailOTPSerializer
from promo.models import Referral
from send_email_otp.models import EmailOtp
from send_email_otp.models import EmailOtp
from django.core.exceptions import PermissionDenied
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()



def generate_referral_code():
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choices(letters_and_digits, k=9))


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user_view(request):
    data = request.data
    serializer = UserSerializer(data=data)

    username = data.get('username')
    email = data.get('email')
    phone_number = data.get('phone_number')

    try:
        user_with_username = User.objects.get(username=username) 
        if user_with_username.is_verified:
            return Response({'detail': 'A user with this username already exists.'}, status=status.HTTP_400_BAD_REQUEST) 
    except User.DoesNotExist:
        pass

    try:
        user_with_email_not_verified = User.objects.get(email=email)
        if not user_with_email_not_verified.is_verified:
            return Response({'detail': 'A user with this email already exists but not verified. Login to verify your account.'}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        pass

    try:
        user_with_email = User.objects.get(email=email)
        if user_with_email.is_verified:
            return Response({'detail': 'A user with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        pass

    try:
        user_with_phone = User.objects.get(phone_number=phone_number) 
        if user_with_phone.is_verified:
            return Response({'detail': 'A user with this phone number already exists.'}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        pass

    if serializer.is_valid():
        print('\nCreating user...')
        user = User.objects.create_user(
            username=username,  
            email=email,
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            phone_number=data.get('phone_number'),
            password=data.get('password'),
            is_terms_conditions_read=data.get('is_terms_conditions_read'),
        )

        try:
            url = settings.MCDOFSHOP_URL
            print('url:', url)
            user.referral_code = generate_referral_code()
            user.save()

            referral_link =  f"{url}/register?ref={user.referral_code}" 
            user.referral_link = referral_link
            user.save()
        except Exception as e:
            print(e)

        # Check if the user has a referral code in the URL
        referral_code = data.get('referral_code')
        print('referral_code:', referral_code)
        
        if referral_code:
            try:
                # Find the user associated with the referral code
                referrer = User.objects.get(referral_code=referral_code) 
                
                # Check if a Referral object already exists for the referrer
                referral, created = Referral.objects.get_or_create(referrer=referrer)
                
                # Add the user to the referrer's referred_users ManyToMany field
                referral.referred_users.add(user)
                # referral.user_count += 1
                
                # Save the referrer instance
                referrer.save()
                print('user added to referred_users of referrer:', user)
            except User.DoesNotExist:
                pass


            print('\nUser created! Verify your email.')
            # Now, based on whether the user is verified or not, set the response status and message
        if user.is_verified:
            return Response({'detail': 'User already exists. Please login.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'User created. Please verify your email.'}, status=status.HTTP_201_CREATED)
            # return Response({'detail': 'User created. Please verify your email.'}, status=status.HTTP_200_OK)
    else:
        print('Error creating user.')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class GoogleLogin(SocialLoginView):
    # permission_classes = [AllowAny]  
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    serializer_class = GoogleLoginSerializer  
    # callback_url = "http://localhost:3000"
    # serializer_class = SocialLoginSerializer
    # serializer_class = MyTokenObtainPairSerializer


#     def get_serializer(self, *args, **kwargs):
#         serializer_class = self.get_serializer_class()
#         kwargs['context'] = self.get_serializer_context()
#         return serializer_class(*args, **kwargs)


# google_login = GoogleLogin.as_view()


# from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
# from allauth.socialaccount.providers.oauth2.views import OAuth2LoginView
# from rest_framework_simplejwt.views import TokenObtainPairView
# from .serializers import MyTokenObtainPairSerializer

# class LoginWithGoogleView(GoogleOAuth2Adapter, OAuth2LoginView):
#     callback_url = 'your-callback-url'
    
#     def complete_login(self, request, app, token, **kwargs):
#         response = super().complete_login(
#             request, app, token, **kwargs)
        
#         # Assuming user info retrieval logic is implemented in get_user_info
#         user_info = self.get_user_info(token.token)

#         if user_info:
#             serializer = MyTokenObtainPairSerializer(data=user_info)
#             serializer.is_valid(raise_exception=True)
#             response.data = serializer.validated_data

#         return response


# from allauth.socialaccount.providers.oauth2.views import (OAuth2Adapter, OAuth2LoginView, OAuth2CallbackView)
# from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
# from rest_framework_simplejwt.views import TokenObtainPairView


# class LoginWithGoogleView(GoogleOAuth2Adapter, OAuth2LoginView):
#     callback_url = 'your-callback-url'

#     def complete_login(self, request, app, token, **kwargs):
#         response = super().complete_login(
#             request, app, token, **kwargs)
#         access_token = token.token
#         refresh_token = token.token_secret

#         user_info = self.get_user_info(access_token)

#         if user_info:
#             user = self.get_provider().sociallogin_from_response(request, user_info)
#             user_info['email'] = user.email  # Ensure email is included
#             user_info['access_token'] = access_token
#             user_info['refresh_token'] = refresh_token

#             # Generate the access token
#             access_token_data = {
#                 'user_id': user.id,
#                 'email': user_info['email'],
#                 'username': user_info['email'],  # Use email as username
#                 'access_token': access_token,
#             }
#             access_token_serializer = UserSerializer(data=access_token_data)
#             access_token_serializer.is_valid(raise_exception=True)

#             # Generate the refresh token
#             refresh = RefreshToken.for_user(user)

#             response.data.update({
#                 'access_token': str(refresh.access_token),
#                 'refresh_token': str(refresh),
#                 'user': access_token_serializer.validated_data
#             })
#         return response



class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=204)
        except Exception as e:
            return Response({"error": "Invalid token"}, status=400)


class GetUserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
class UpdateUserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = UpdateUserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Profile updated successfully.'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserAvatarView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = AvatarUpdateSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            # Check if the user making the request matches the user being updated
            if user.id == serializer.validated_data.get('id'):
                # Handle avatar update here
                if 'avatar' in request.FILES:
                    user.avatar = request.FILES['avatar']
                user.save()
                
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                raise PermissionDenied("You don't have permission to update this user.")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        user = request.user
        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']
        
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response({'detail': 'Password changed successfully.'})
        else:
            return Response({'detail': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AccountDeleteView(APIView): 
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DeleteAccountSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            password = serializer.validated_data['password']

            if user.check_password(password):
                user.delete()
                return Response({'detail': 'Account deleted successfully.'})
            else:
                return Response({'detail': 'Incorrect password.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
