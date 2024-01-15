# from django.contrib import admin
# from . import models


# @admin.register(models.Product)
# class AuthorAdmin(admin.ModelAdmin):
#     list_display = ('name', '_id', 'price', 'promo_price', 'promo_code', 'save_count', 'view_count', 'countInStock', 'rating', 'numReviews', 'createdAt', )  
#     search_fields = ('name',)

#     # def get_readonly_fields(self, request, obj=None):
#     #     readonly_fields = ['price', 'promo_price', 'save_count', 'view_count', 'rating', 'numReviews', 'createdAt']
#     #     if obj and obj.is_superuser:
#     #         readonly_fields.remove('price', 'promo_price')
#     #     return readonly_fields


# @admin.register(models.Order)
# class AuthorAdmin(admin.ModelAdmin):
#     list_display = ('order_id', 'createdAt', 'user', 'totalPrice', 'promo_discount', 'promo_total_price', 'isPaid', 'paymentMethod', 'isDelivered') 
#     search_fields = ('order_id',)

#     # def get_readonly_fields(self, request, obj=None):
#     #     readonly_fields = ['price', 'promo_price', 'save_count', 'view_count', 'rating', 'numReviews', 'createdAt']
#     #     if obj and obj.is_superuser:
#     #         readonly_fields.remove('price', 'promo_price')
#     #     return readonly_fields
    

# @admin.register(models.Review)
# class AuthorAdmin(admin.ModelAdmin):
#     list_display = ('product', 'name', 'rating', 'user', 'comment') 

#     # def get_readonly_fields(self, request, obj=None):
#     #     readonly_fields = ['price', 'promo_price', 'save_count', 'view_count', 'rating', 'numReviews', 'createdAt']
#     #     if obj and obj.is_superuser:
#     #         readonly_fields.remove('price', 'promo_price')
#     #     return readonly_fields
  

# @admin.register(models.ShippingAddress)
# class AuthorAdmin(admin.ModelAdmin):
#     list_display = ('address', 'order', 'city', 'shippingPrice') 

#     # def get_readonly_fields(self, request, obj=None):
#     #     readonly_fields = ['price', 'promo_price', 'save_count', 'view_count', 'rating', 'numReviews', 'createdAt']
#     #     if obj and obj.is_superuser:
#     #         readonly_fields.remove('price', 'promo_price')
#     #     return readonly_fields


# @admin.register(models.OrderItem)
# class AuthorAdmin(admin.ModelAdmin):
#     list_display = ('_id', 'product', 'order', 'qty', 'price', 'image') 

#     # def get_readonly_fields(self, request, obj=None):
#     #     readonly_fields = ['price', 'promo_price', 'save_count', 'view_count', 'rating', 'numReviews', 'createdAt']
#     #     if obj and obj.is_superuser:
#     #         readonly_fields.remove('price', 'promo_price')
#     #     return readonly_fields
