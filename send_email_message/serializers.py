from django.db import models
from rest_framework import serializers
from .models import SendEmailMessage

from django.contrib.auth import get_user_model

User = get_user_model()  

class SendEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SendEmailMessage
        fields = '__all__'
        