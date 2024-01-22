# marketplace/models.py 
from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model() 

BUSINESS_TYPE_CHOICES = [ 
        ('Registered', 'Registered'),
        ('Unregistered', 'Unregistered'),  
    ]

STAFF_SIZE_CHOICES = [
        ('Small', 'Small (1-50 employees)'),
        ('Medium', 'Medium (51-250 employees)'), 
        ('Large', 'Large (251+ employees)'),
    ]

BUSINESS_INDUSTRY_CHOICES = [
        ('Information Technology', 'Information Technology'), 
        ('Healthcare', 'Healthcare'),
        ('Finance', 'Finance'),
        ('Education', 'Education'),
        ('Retail', 'Retail'),
        ('Manufacturing', 'Manufacturing'),
        ('Services', 'Services'),
        ('Entertainment', 'Entertainment'),
        ('Food', 'Food & Beverage'),
        ('Travel', 'Travel & Tourism'),
        ('Real Estate', 'Real Estate'),
        ('Construction', 'Construction'),
        ('Automotive', 'Automotive'),
        ('Agriculture', 'Agriculture'),
        ('Energy', 'Energy'),
        ('Environmental', 'Environmental'),
        ('Government', 'Government'),
        ('Nonprofit', 'Nonprofit'),
        ('Others', 'Others'),
    ]

BUSINESS_CATEGORY_CHOICES = [
  ('Startup', 'Startup'),
  ('Small Business', 'Small Business'),
  ('Medium Business', 'Medium Business'),
  ('Large Business', 'Large Business'),
  ('Corporation', 'Corporation'),
  ('Sole Proprietorship', 'Sole Proprietorship'),
  ('Partnership', 'Partnership'),
  ('Franchise', 'Franchise'),
  ('Family Owned', 'Family Owned'),
  ('Online Business', 'Online Business'),
  ('Brick and Mortar', 'Brick and Mortar'),
  ('Service Provider', 'Service Provider'),
  ('Retailer', 'Retailer'),
  ('Wholesaler', 'Wholesaler'),
  ('Manufacturer', 'Manufacturer'),
  ('Restaurant', 'Restaurant'),
  ('Hospitality', 'Hospitality'),
  ('Healthcare', 'Healthcare'),
  ('Education', 'Education'),
  ('Tech', 'Tech'),
  ('Creative', 'Creative'),
  ('Entertainment', 'Entertainment'),
  ('Travel', 'Travel'),
  ('Construction', 'Construction'),
  ('Automotive', 'Automotive'),
  ('Agriculture', 'Agriculture'),
  ('Energy', 'Energy'),
  ('Environmental', 'Environmental'),
  ('Government', 'Government'),
  ('Nonprofit', 'Nonprofit'),
  ('Others', 'Others'),
]

ID_TYPE_CHOICES = [
    # ('NIN', 'NIN'),
    ('Intl Passport', 'Intl Passport'), 
    ('Driving License', 'Driving License'),
    ('Govt Issued ID', 'Govt Issued ID'),
]

DURATION_CHOICES = (
    ('0 day', '0 day'),
    ('1 day', '1 day'),
    ('2 days', '2 days'),
    ('3 days', '3 days'),
    ('5 days', '5 days'),
    ('1 week', '1 week'),
    ('2 weeks', '2 weeks'),
    ('1 month', '1 month'),
)

AD_CONDITION_CHOICES = (
    ('Brand New', 'Brand New'),
    ('Fairly Used', 'Fairly Used'),
)

AD_CATEGORY_CHOICES = [
    ('Home Appliances', 'Home Appliances'),
    ('Properties', 'Properties'),
    ('Electronics', 'Electronics'),
    ('Fashion', 'Fashion'),
    ('Vehicles', 'Vehicles'),
    ('Services', 'Services'),
    ('Mobile Phones', 'Mobile Phones'),
    ('Health & Beauty', 'Health & Beauty'),
    ('Sports', 'Sports'),
    ('Jobs', 'Jobs'),
    ('Babies and Kids', 'Babies and Kids'),
    ('Agric & Food', 'Agric & Food'),
    ('Repairs', 'Repairs'),
    ('Equipment & Tools', 'Equipment & Tools'),
    ('CVs', 'CVs'),
    ('Pets', 'Pets'),
    ('Others', 'Others'),
]

AD_TYPE_CHOICES = [
    # Choices for Home Appliances
    ("Washing Machine", "Washing Machine"),
    ("Refrigerator", "Refrigerator"),
    ("Microwave", "Microwave"),
    ("Coffee Machine", "Coffee Machine"),
    ("Air Conditioner", "Air Conditioner"),
    ("Solar", "Solar"),
    ("Kitchen Appliances", "Kitchen Appliances"),

    # Choices for Properties
    ("House", "House"),
    ("Apartment", "Apartment"),
    ("Land", "Land"),
    ("Commercial Property", "Commercial Property"),

    # Choices for Electronics
    ("Laptop", "Laptop"),
    ("Smartphone", "Smartphone"),
    ("Camera", "Camera"),
    ("Headphones", "Headphones"),
    ("Television", "Television"),

    # Choices for Fashion
    ("Clothing", "Clothing"),
    ("Shoes", "Shoes"),
    ("Accessories", "Accessories"),

    # Choices for Vehicles
    ("Car", "Car"),
    ("Motorcycle", "Motorcycle"),
    ("Bicycle", "Bicycle"),

    # Choices for Services
    ("Cleaning", "Cleaning"),
    ("Plumbing", "Plumbing"),
    ("Electrician", "Electrician"),
    ("Catering", "Catering"),
    ("Tutoring", "Tutoring"),

    # Choices for Mobile Phones
    ("iPhone", "iPhone"),
    ("Samsung", "Samsung"),
    ("Google Pixel", "Google Pixel"),
    ("OnePlus", "OnePlus"),

    # Choices for Health & Beauty
    ("Skincare", "Skincare"),
    ("Haircare", "Haircare"),
    ("Makeup", "Makeup"),
    ("Fitness Equipment", "Fitness Equipment"),

    # Choices for Sports
    ("Soccer", "Soccer"),
    ("Basketball", "Basketball"),
    ("Tennis", "Tennis"),
    ("Golf", "Golf"),

    # Choices for Jobs
    ("IT", "IT"),
    ("Sales", "Sales"),
    ("Marketing", "Marketing"),
    ("Administrative", "Administrative"),

    # Choices for Babies and Kids
    ("Toys", "Toys"),
    ("Clothing Kids", "Clothing"),
    ("Strollers", "Strollers"),

    # Choices for Agric & Food
    ("Farm Products", "Farm Products"),
    ("Processed Food", "Processed Food"),
    ("Beverages", "Beverages"),

    # Choices for Repairs
    ("Electronic Repair", "Electronic Repair"),
    ("Appliance Repair", "Appliance Repair"),
    ("Car Repair", "Car Repair"),

    # Choices for Equipment & Tools
    ("Power Tools", "Power Tools"),
    ("Hand Tools", "Hand Tools"),
    ("Kitchen Tools", "Kitchen Tools"),

    # Choices for CVs
    ("Engineering", "Engineering"),
    ("Marketing CVs", "Marketing"),
    ("Design", "Design"),
    ("Education", "Education"),

    # Choices for Pets
    ("Dog", "Dog"),
    ("Cat", "Cat"),
    ("Fish", "Fish"),
    ("Bird", "Bird"),

    # Choices for Others
    ("Others", "Others"),
]

CURRENCY_CHOICES = (
    ('NGN', 'NGN'),
    ('USD', 'USD'),
    ('CAD', 'CAD'),
    ('EUR', 'EUR'),
    ('GBP', 'GBP'),
    ('GHS', 'GHS'),
    ('INR', 'INR'),
    ('CNY', 'CNY'),
    ('ZAR', 'ZAR'),
    ('AED', 'United Arab Emirates Dirham'),
    ('AUD', 'Australian Dollar'),
    ('BRL', 'Brazilian Real'),
    ('JPY', 'Japanese Yen'),
    ('KES', 'Kenyan Shilling'),
    ('SAR', 'Saudi Riyal'),
    # Additional currencies sorted alphabetically
    ('AFN', 'Afghan Afghani'),
    ('ALL', 'Albanian Lek'),
    ('AMD', 'Armenian Dram'),
    ('ANG', 'Netherlands Antillean Guilder'),
    ('AOA', 'Angolan Kwanza'),
    ('ARS', 'Argentine Peso'),
    ('AWG', 'Aruban Florin'),
    ('AZN', 'Azerbaijani Manat'),
    ('BAM', 'Bosnia-Herzegovina Convertible Mark'),
    ('BBD', 'Barbadian Dollar'),
    ('BDT', 'Bangladeshi Taka'),
    ('BGN', 'Bulgarian Lev'),
    ('BHD', 'Bahraini Dinar'),
    ('BIF', 'Burundian Franc'),
    ('BMD', 'Bermudian Dollar'),
    ('BND', 'Brunei Dollar'),
    ('BOB', 'Bolivian Boliviano'),
    ('BSD', 'Bahamian Dollar'),
    ('BTN', 'Bhutanese Ngultrum'),
    ('BWP', 'Botswanan Pula'),
    ('BYN', 'Belarusian Ruble'),
    ('BZD', 'Belize Dollar'),
    ('CDF', 'Congolese Franc'),
    ('CHF', 'Swiss Franc'),
    ('CLP', 'Chilean Peso'),
    ('COP', 'Colombian Peso'),
    ('CRC', 'Costa Rican Colón'),
    ('CUP', 'Cuban Peso'),
    ('CVE', 'Cape Verdean Escudo'),
    ('CZK', 'Czech Republic Koruna'),
    ('DJF', 'Djiboutian Franc'),
    ('DKK', 'Danish Krone'),
    ('DOP', 'Dominican Peso'),
    ('DZD', 'Algerian Dinar'),
    ('EGP', 'Egyptian Pound'),
    ('ERN', 'Eritrean Nakfa'),
    ('ETB', 'Ethiopian Birr'),
    ('FJD', 'Fijian Dollar'),
    ('FKP', 'Falkland Islands Pound'),
    ('FOK', 'Faroe Islands Króna'),
    ('GEL', 'Georgian Lari'),
    ('GGP', 'Guernsey Pound'),
    ('GIP', 'Gibraltar Pound'),
    ('GMD', 'Gambian Dalasi'),
    ('GNF', 'Guinean Franc'),
    ('GTQ', 'Guatemalan Quetzal'),
    ('GYD', 'Guyanaese Dollar'),
    ('HKD', 'Hong Kong Dollar'),
    ('HNL', 'Honduran Lempira'),
    ('HRK', 'Croatian Kuna'),
    ('HTG', 'Haitian Gourde'),
    ('HUF', 'Hungarian Forint'),
    ('IDR', 'Indonesian Rupiah'),
    ('ILS', 'Israeli New Shekel'),
    ('IMP', 'Isle of Man Pound'),
    ('IQD', 'Iraqi Dinar'),
    ('IRR', 'Iranian Rial'),
    ('ISK', 'Icelandic Króna'),
    ('JEP', 'Jersey Pound'),
    ('JMD', 'Jamaican Dollar'),
    ('JOD', 'Jordanian Dinar'),
    ('KGS', 'Kyrgystani Som'),
    ('KHR', 'Cambodian Riel'),
    ('KID', 'Kiribati Dollar'),
    ('KWD', 'Kuwaiti Dinar'),
    ('KYD', 'Cayman Islands Dollar'),
    ('KZT', 'Kazakhstani Tenge'),
    ('LAK', 'Laotian Kip'),
    ('LBP', 'Lebanese Pound'),
    ('LKR', 'Sri Lankan Rupee'),
    ('LRD', 'Liberian Dollar'),
    ('LSL', 'Lesotho Loti'),
    ('LYD', 'Libyan Dinar'),
    ('MAD', 'Moroccan Dirham'),
    ('MDL', 'Moldovan Leu'),
    ('MGA', 'Malagasy Ariary'),
    ('MKD', 'Macedonian Denar'),
    ('MMK', 'Myanma Kyat'),
    ('MNT', 'Mongolian Tugrik'),
    ('MOP', 'Macanese Pataca'),
    ('MRU', 'Mauritanian Ouguiya'),
    ('MUR', 'Mauritian Rupee'),
    ('MVR', 'Maldivian Rufiyaa'),
    ('MWK', 'Malawian Kwacha'),
    ('MXN', 'Mexican Peso'),
    ('MYR', 'Malaysian Ringgit'),
    ('MZN', 'Mozambican Metical'),
    ('NAD', 'Namibian Dollar'),
    ('NIO', 'Nicaraguan Córdoba'),
    ('NOK', 'Norwegian Krone'),
    ('NPR', 'Nepalese Rupee'),
    ('NZD', 'New Zealand Dollar'),
    ('OMR', 'Omani Rial'),
    ('PAB', 'Panamanian Balboa'),
    ('PEN', 'Peruvian Nuevo Sol'),
    ('PGK', 'Papua New Guinean Kina'),
    ('PHP', 'Philippine Peso'),
    ('PKR', 'Pakistani Rupee'),
    ('PLN', 'Polish Złoty'),
    ('PYG', 'Paraguayan Guarani'),
    ('QAR', 'Qatari Rial'),
    ('RON', 'Romanian Leu'),
    ('RSD', 'Serbian Dinar'),
    ('RUB', 'Russian Ruble'),
    ('RWF', 'Rwandan Franc'),
    ('SBD', 'Solomon Islands Dollar'),
    ('SCR', 'Seychellois Rupee'),
    ('SDG', 'Sudanese Pound'),
    ('SEK', 'Swedish Krona'),
    ('SGD', 'Singapore Dollar'),
    ('SHP', 'Saint Helena Pound'),
    ('SLL', 'Sierra Leonean Leone'),
    ('SOS', 'Somali Shilling'),
    ('SRD', 'Surinamese Dollar'),
    ('SSP', 'South Sudanese Pound'),
    ('STN', 'São Tomé and Príncipe Dobra'),
    ('SYP', 'Syrian Pound'),
    ('SZL', 'Swazi Lilangeni'),
    ('TJS', 'Tajikistani Somoni'),
    ('TMT', 'Turkmenistani Manat'),
    ('TND', 'Tunisian Dinar'),
    ('TOP', 'Tongan Paʻanga'),
    ('TRY', 'Turkish Lira'),
    ('TTD', 'Trinidad and Tobago Dollar'),
    ('TVD', 'Tuvaluan Dollar'),
    ('TWD', 'New Taiwan Dollar'),
    ('TZS', 'Tanzanian Shilling'),
    ('UAH', 'Ukrainian Hryvnia'),
    ('UGX', 'Ugandan Shilling'),
    ('UYU', 'Uruguayan Peso'),
    ('UZS', 'Uzbekistan Som'),
    ('VES', 'Venezuelan Bolívar'),
    ('VND', 'Vietnamese Đồng'),
    ('VUV', 'Vanuatu Vatu'),
    ('WST', 'Samoan Tala'),
    ('XAF', 'Central African CFA Franc'),
    ('XCD', 'Eastern Caribbean Dollar'),
    ('XDR', 'Special Drawing Rights'),
    ('XOF', 'West African CFA franc'),
    ('XPF', 'CFP Franc'),
    ('YER', 'Yemeni Rial'),
    ('ZMW', 'Zambian Kwacha'),
)

MAIN_CURRENCY_CHOICES = (
    ('NGN', 'NGN'),
    ('USD', 'USD'),
)

AD_REPORT_CHOICES = (
    ('Misleading Content', 'False or deceptive information in the ad, claims that are not substantiated.'),
    ('Inappropriate Content', 'Offensive language, images, or themes; content violating community standards or guidelines.'),
    ('Irrelevant or Unwanted Ads', 'Ads that are not relevant to the user; too frequent display of the same ad.'),
    ('Malware or Phishing', 'Ads containing malicious software or links to phishing websites.'),
    ('Privacy Concerns', 'Collection of personal information without consent; violation of privacy policies.'),
    ('Low-Quality or Unprofessional Design', 'Poorly designed or unprofessional-looking ads.'),
    ('Counterfeit or Fraudulent Products', 'Ads promoting counterfeit goods or fraudulent services.'),
    ('Political or Social Issues', 'Ads perceived as promoting hate speech, discrimination, or controversial political content.'),
    ('Technical Issues', 'Broken links or malfunctioning interactive elements in the ad.'),
    ('Unsolicited or Spammy Ads', 'Ads that appear as spam or unsolicited marketing messages.'),
    ('Disallowed Content', 'Ads promoting content that violates platform policies or legal regulations.'),
    ('Unverified Claims', 'Ads making claims that cannot be verified or proven.'),
    ('Unrealistic Promises', 'Ads promising unrealistic results or benefits.'),
)


class MarketPlaceSellerAccount(models.Model):
    seller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="seller_account_user")
    business_name = models.CharField(max_length=100, null=True)
    business_status = models.CharField(max_length=225, null=True, choices=BUSINESS_TYPE_CHOICES)
    business_reg_num = models.CharField(max_length=50, null=True, blank=True)
    business_reg_cert = models.ImageField(upload_to='media/sellers/', null=True, blank=True)
    business_address = models.CharField(max_length=225, null=True)
    staff_size = models.CharField( max_length=50, null=True, choices=STAFF_SIZE_CHOICES)
    business_industry = models.CharField( max_length=50, null=True, choices=BUSINESS_INDUSTRY_CHOICES)    
    business_category = models.CharField( max_length=50, null=True, choices=BUSINESS_CATEGORY_CHOICES)
    business_description = models.TextField(max_length=225, null=True, blank=True)
    business_phone = models.CharField(max_length=20, null=True, blank=True)
    business_website = models.CharField(max_length=225, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    id_type = models.CharField( max_length=50, null=True, blank=True, choices=ID_TYPE_CHOICES)    
    id_number = models.CharField(max_length=30, null=True)
    id_card_image = models.ImageField(upload_to='media/sellers/')
    dob = models.CharField(max_length=225, null=True, blank=True)
    home_address = models.CharField(max_length=225, null=True, blank=True)
    is_seller_verified = models.BooleanField(default=False)
    is_seller_banned = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, editable=False)
    review = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.seller}"

    def get_ad_count(self):
        return PostFreeAd.objects.filter(seller=self.seller).count()


class MarketplaceSellerPhoto(models.Model):
    seller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="photo_seller")  
    photo = models.ImageField(upload_to='media/sellers/')
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self): 
        return f'Photo {self.pk}'


class PostFreeAd(models.Model): 
    seller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="ad_seller") 
    # user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="fre_ad_reporter") 
    # seller_photo = models.ForeignKey(MarketplaceSellerPhoto, on_delete=models.SET_NULL, null=True, blank=True, related_name="seller_free_ad_photo") 
    ad_name = models.CharField(max_length=80, null=True)
    ad_category = models.CharField(max_length=100, choices=AD_CATEGORY_CHOICES, null=True) 
    ad_type = models.CharField(max_length=100, choices=AD_TYPE_CHOICES, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True)
    state_province = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    condition = models.CharField(max_length=100, choices=AD_CONDITION_CHOICES, null=True, blank=True)
    # ad_charges = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    currency = models.CharField(max_length=50, choices=CURRENCY_CHOICES, default='NGN', null=True, blank=True)
    price = models.DecimalField(max_digits=16, decimal_places=2, null=True)
    usd_price = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True)
    is_price_negotiable = models.BooleanField(default=False)
    promo_price = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True)    
    brand = models.CharField(max_length=255, blank=True, null=True) 
    description = models.TextField(max_length=4000, blank=True, null=True)
    youtube_link = models.URLField(max_length=255, blank=True, null=True)
    # promo_code = models.ForeignKey('promo.PromoCode', on_delete=models.SET_NULL, null=True, blank=True)
    ad_rating = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, editable=False)
    num_reviews = models.IntegerField(null=True, blank=True, default=0, editable=False)
    ad_save_count = models.PositiveIntegerField(default=0, editable=False)
    phone_view_count = models.PositiveIntegerField(default=0, editable=False)
    phone_view_user_count = models.PositiveIntegerField(default=0, editable=False)
    ad_view_count = models.PositiveIntegerField(default=0, editable=False)
    count_in_stock = models.IntegerField(null=True, blank=True)
    ad_count = models.PositiveIntegerField(default=0, editable=False)
    is_active = models.BooleanField(default=False)
    is_ad_reported = models.BooleanField(default=False)
    ad_report_count = models.PositiveIntegerField(default=0, editable=False)
    ad_report = models.CharField(max_length=100, choices=AD_REPORT_CHOICES, null=True, blank=True)
    image1 = models.ImageField(upload_to='./media/marketplace', null=True, blank=True)
    image2 = models.ImageField(upload_to='./media/marketplace', null=True, blank=True)
    image3 = models.ImageField(upload_to='./media/marketplace', null=True, blank=True)
    duration = models.CharField(max_length=100, choices=DURATION_CHOICES, default='1 day', null=True, blank=True)
    duration_hours = models.DurationField(null=True, blank=True)
    expiration_date = models.DateTimeField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True) 

    def save(self, *args, **kwargs):
        if self.duration:
            if self.duration == '0 day':
                self.duration_hours = timedelta(hours=0)
            elif self.duration == '1 day':
                self.duration_hours = timedelta(hours=24)
            elif self.duration == '2 days':
                self.duration_hours = timedelta(days=2)
            elif self.duration == '3 days':
                self.duration_hours = timedelta(days=3)
            elif self.duration == '5 days':
                self.duration_hours = timedelta(days=5)
            elif self.duration == '1 week':
                self.duration_hours = timedelta(weeks=1)
            elif self.duration == '2 weeks':
                self.duration_hours = timedelta(weeks=2)
            elif self.duration == '1 month':
                self.duration_hours = timedelta(days=30)  

            self.expiration_date = datetime.now() + self.duration_hours
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.ad_name


class PostPaidAd(models.Model):
    seller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="paid_ad_seller") 
    # user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="paid_ad_reporter") 
    # seller_photo = models.ForeignKey(MarketplaceSellerPhoto, on_delete=models.SET_NULL, null=True, blank=True, related_name="seller_paid_ad_photo") 
    ad_name = models.CharField(max_length=80, null=True)
    ad_category = models.CharField(max_length=100, choices=AD_CATEGORY_CHOICES, null=True, blank=True)
    ad_type = models.CharField(max_length=100, choices=AD_TYPE_CHOICES, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    state_province = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    condition = models.CharField(max_length=100, choices=AD_CONDITION_CHOICES, null=True, blank=True)
    currency = models.CharField(max_length=50, choices=MAIN_CURRENCY_CHOICES, default='NGN', null=True, blank=True)
    price = models.DecimalField(max_digits=16, decimal_places=2, null=True)
    usd_price = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True)
    usd_currency = models.CharField(max_length=50, choices=CURRENCY_CHOICES, default='USD', null=True)
    promo_price = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True)    
    brand = models.CharField(max_length=255, blank=True, null=True) 
    promo_code = models.CharField(max_length=10, null=True, blank=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=1, default=0) 
    description = models.TextField(max_length=4000, blank=True, null=True)
    youtube_link = models.URLField(max_length=255, blank=True, null=True)
    ad_charges = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    is_price_negotiable = models.BooleanField(default=False)
    phone_view_count = models.PositiveIntegerField(default=0, editable=False)
    phone_view_user_count = models.PositiveIntegerField(default=0, editable=False)
    ad_rating = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, editable=False)
    num_reviews = models.IntegerField(null=True, blank=True, default=0, editable=False)
    ad_save_count = models.PositiveIntegerField(default=0, editable=False)
    ad_view_count = models.PositiveIntegerField(default=0, editable=False)
    count_in_stock = models.IntegerField(null=True, blank=True)
    ad_count = models.PositiveIntegerField(default=0, editable=False)
    is_auto_renewal = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_ad_reported = models.BooleanField(default=False)
    ad_report_count = models.PositiveIntegerField(default=0, editable=False)
    ad_report = models.CharField(max_length=100, choices=AD_REPORT_CHOICES, null=True, blank=True)
    image1 = models.ImageField(upload_to='./media/marketplace', null=True, default='./media/default_ad_photo.jpg')
    image2 = models.ImageField(upload_to='./media/marketplace', null=True, blank=True)
    image3 = models.ImageField(upload_to='./media/marketplace', null=True, blank=True)
    duration = models.CharField(max_length=100, choices=DURATION_CHOICES, default='1 day', null=True, blank=True)
    duration_hours = models.DurationField(null=True, blank=True)
    expiration_date = models.DateTimeField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True) 

    def save(self, *args, **kwargs):
        if self.duration:
            if self.duration == '0 day':
                self.duration_hours = timedelta(hours=0)
            elif self.duration == '1 day':
                self.duration_hours = timedelta(hours=24)
            elif self.duration == '2 days':
                self.duration_hours = timedelta(days=2)
            elif self.duration == '3 days':
                self.duration_hours = timedelta(days=3)
            elif self.duration == '5 days':
                self.duration_hours = timedelta(days=5)
            elif self.duration == '1 week':
                self.duration_hours = timedelta(weeks=1)
            elif self.duration == '2 weeks':
                self.duration_hours = timedelta(weeks=2)
            elif self.duration == '1 month':
                self.duration_hours = timedelta(days=30)  

            self.expiration_date = datetime.now() + self.duration_hours
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.ad_name

   
class PaysofterApiKey(models.Model):
    seller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="paysofter_seller") 
    live_api_key = models.CharField(max_length=100, null=True, blank=True)
    is_api_key_live = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="message_user")
    free_ad = models.ForeignKey(PostFreeAd, on_delete=models.CASCADE, related_name='free_ad_message', blank=True, null=True)
    paid_ad = models.ForeignKey(PostPaidAd, on_delete=models.CASCADE, related_name='paid_ad_message', blank=True, null=True)
    message = models.TextField(max_length=500, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return f"{self.user} | {self.message}"


class ReportFreeAd(models.Model): 
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="fre_ad_reporter") 
    free_ad = models.ForeignKey(PostFreeAd, on_delete=models.CASCADE, related_name='free_ad_report', blank=True, null=True)
    ad_report = models.CharField(max_length=100, choices=AD_REPORT_CHOICES, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

 
class ReportPaidAd(models.Model): 
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="paid_ad_reporter") 
    paid_ad = models.ForeignKey(PostPaidAd, on_delete=models.CASCADE, related_name='paid_ad_report', blank=True, null=True)
    ad_report = models.CharField(max_length=100, choices=AD_REPORT_CHOICES, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
 