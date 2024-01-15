# user_profile/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
# from app.models import Product

class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field.""" 

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password.""" 
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    phone_number = models.CharField(max_length=18, unique=True)
    is_verified = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='images/avatars/', null=True, blank=True) 
    favorite_products = models.ManyToManyField('app.Product', related_name='favorited_by', editable=False) 
    viewed_products = models.ManyToManyField('app.Product', related_name='viewed_products', editable=False)  
    referral_code = models.CharField(max_length=10, unique=True, null=True) 
    referral_link = models.CharField(max_length=225, unique=True, null=True)
    # referred_users = models.ManyToManyField('promo.Referral', related_name='referred_users')   
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)  
    is_marketplace_seller = models.BooleanField(default=False)  
    is_ecommerce_seller = models.BooleanField(default=False)  
    is_terms_conditions_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, blank=True, editable=False) 
  
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'phone_number']

    # def save(self, *args, **kwargs):
    #     # Set the username to be the same as the email
    #     self.username = self.email
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.email
 
    objects = CustomUserManager()

    class Meta: 
        default_related_name = 'user'


# class CustomUserManager(BaseUserManager):
#     """Define a model manager for User model with no username field."""

#     def _create_user(self, email, password=None, **extra_fields):
#         """Create and save a User with the given email and password."""
#         if not email:
#             raise ValueError('The given email must be set')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_user(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', False)
#         extra_fields.setdefault('is_superuser', False)
#         return self._create_user(email, password, **extra_fields)

#     def create_superuser(self, email, password=None, **extra_fields):
#         """Create and save a SuperUser with the given email and password."""
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)

#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')

#         return self._create_user(email, password, **extra_fields)
    
# class User(AbstractUser):
#     email = models.EmailField(max_length=100, unique=True)
#     phone_number = models.CharField(max_length=15, unique=True)
#     is_verified = models.BooleanField(default=False)
#     avatar = models.ImageField(upload_to='images/avatars/', null=True, blank=True)
#     # favorites = models.ManyToManyField(Product, related_name='favorited_by')
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#     created_at = models.DateTimeField(default=timezone.now, blank=True)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['first_name', 'phone_number']
 
#     objects = CustomUserManager()

#     class Meta: 
#         default_related_name = 'user'
