# live_chat/serializers.py
from rest_framework import serializers
from .models import ChatRoom, ChatMessage

class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = '__all__'

class ChatMessageSerializer(serializers.ModelSerializer): 
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    class Meta:
        model = ChatMessage
        fields = '__all__'


# from rest_framework import serializers
# from .models import ChatMessage

# class ChatMessageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ChatMessage
#         fields = '__all__'
