# user_profile/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
# from io import BytesIO
# from django.core.files import File
# from PIL import Image, ImageDraw
# import qrcode

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

    saved_free_ads = models.ManyToManyField('marketplace.PostFreeAd', related_name='saved_free_ads', editable=False) 
    saved_paid_ads = models.ManyToManyField('marketplace.PostPaidAd', related_name='saved_paid_ads', editable=False) 
    viewed_free_ads = models.ManyToManyField('marketplace.PostFreeAd', related_name='viewed_free_ads', editable=False)
    viewed_paid_ads = models.ManyToManyField('marketplace.PostPaidAd', related_name='viewed_paid_ads', editable=False)  
    seller_followers = models.ManyToManyField('marketplace.MarketPlaceSellerAccount', related_name='seller_followers', 
    editable=False
    )  
    followed_sellers = models.ManyToManyField('marketplace.MarketPlaceSellerAccount', related_name='followed_sellers', 
    editable=False
    )  
    referral_code = models.CharField(max_length=10, unique=True, null=True) 
    referral_link = models.CharField(max_length=225, unique=True, null=True)
    # referred_users = models.ManyToManyField('promo.Referral', related_name='referred_users')     
    # referral_qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)  
    is_marketplace_seller = models.BooleanField(default=False)  
    is_seller_account_verified = models.BooleanField(default=False)
    is_seller_account_disabled = models.BooleanField(default=False)
    is_followed_seller = models.BooleanField(default=False)  
    is_ecommerce_seller = models.BooleanField(default=False)  
    ad_charge_is_owed = models.BooleanField(default=False)
    is_terms_conditions_read = models.BooleanField(default=False)
    
    user_is_not_active = models.BooleanField(default=False)  
    is_user_live_banned = models.BooleanField(default=False)  
    is_user_1day_banned = models.BooleanField(default=False)  
    is_user_2day_banned = models.BooleanField(default=False)  
    is_user_3day_banned = models.BooleanField(default=False)  
    is_user_1week_banned = models.BooleanField(default=False)  
    is_user_3week_banned = models.BooleanField(default=False)  
    is_user_1month_banned = models.BooleanField(default=False)  
    is_user_2month_banned = models.BooleanField(default=False)  
    is_user_3month_banned = models.BooleanField(default=False)  
    is_user_6month_banned = models.BooleanField(default=False)  
    is_user_1year_banned = models.BooleanField(default=False)  

    last_login = models.DateTimeField(null=True, blank=True, auto_now=True)
    created_at = models.DateTimeField(default=timezone.now, blank=True, editable=False) 
  
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 
                       'phone_number', 
                    #    'username'
                       ]

    # def save(self, *args, **kwargs):
    #     # Set the username to be the same as the email
    #     self.username = self.email
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.email

    # def save(self, *args, **kwargs):
    #     # If a referral link exists, generate QR code
    #     if self.referral_link:
    #         qr_code_img = qrcode.make(self.referral_link)
    #         canvas = Image.new('RGB', (290, 290), 'white')
    #         draw = ImageDraw.Draw(canvas)
    #         canvas.paste(qr_code_img)
    #         buffer = BytesIO()
    #         canvas.save(buffer, 'PNG')
    #         self.referral_qr_code.save(f'qr_code_{self.username}.png', File(buffer), save=False)
    #         canvas.close()
        
    #     super().save(*args, **kwargs)
 
    objects = CustomUserManager()

    class Meta: 
        default_related_name = 'user'
