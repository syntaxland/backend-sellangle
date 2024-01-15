from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth import get_user_model

User = get_user_model()

 
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 
                  'last_name', 'password', 'phone_number', 
                  'is_verified', 'is_superuser', 'is_staff', 
                  'is_ecommerce_seller', 'is_marketplace_seller', 'created_at'
                  ]
        extra_kwargs = {
            'password': {'write_only': True},
        }


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializer(self.user).data
        for k, v in serializer.items():
            data[k] = v
        return data


class GoogleLoginSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        email = attrs.get("email")
        google_id = attrs.get("google_id")
        token_id = attrs.get("token_id")

        if not email or not google_id or not token_id:
            raise serializers.ValidationError("Email, google_id, and token_id are required.")

        # Custom authentication logic
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # User doesn't exist, create a new user
            user = User.objects.create_user(email=email, username=email)
            user.google_id = google_id
            user.set_unusable_password()
            user.save()

        # verify the Google login using the token_id ...
        #  use libraries like the google-auth library to validate the token_id
        # e.g. validate_google_token(token_id)

        # After successful authentication, generate tokens
        refresh = RefreshToken.for_user(user)
        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": UserSerializer(user).data,
        }
        return data
    

# class GoogleLoginSerializer(serializers.Serializer):
#     access_token = serializers.CharField()  # This field should match the parameter name you're using

#     def validate(self, attrs):
#         access_token = attrs.get('access_token')
#         user = None

#         try:
#             user = User.objects.get(email='dummy_email@gmail.com')  # Replace with your logic to retrieve or create user
#             # Perform any additional validation or user creation logic here if needed
#         except User.DoesNotExist:
#             pass

#         if user:
#             refresh = RefreshToken.for_user(user)
#             data = {
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#             }
#             return data
#         else:
#             raise serializers.ValidationError("Google login failed. User not found.")

    

class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'token']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)
    

class UpdateUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number']


class AvatarUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  
        fields = ('avatar',)


class ChangePasswordSerializer(serializers.Serializer): 
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class DeleteAccountSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
