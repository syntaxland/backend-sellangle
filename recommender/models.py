# # models.py
# from django.db import models
# from django.contrib.auth import get_user_model
# from app.models import Product

# User = get_user_model() 


# class UserInteraction(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) 
#     interaction_type = models.CharField(
#         max_length=20,
#         choices=[
#             ('save', 'Saved'),
#             ('view', 'Viewed'),
#             # Add more interaction types as needed
#         ],
#     )
#     timestamp = models.DateTimeField(auto_now_add=True)
