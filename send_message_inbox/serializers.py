from django.db import models
from rest_framework import serializers
from .models import SendMessageInbox

from django.contrib.auth import get_user_model

User = get_user_model()  

class SendMessageInboxSerializer(serializers.ModelSerializer):
    class Meta:
        model = SendMessageInbox
        fields = '__all__'
        