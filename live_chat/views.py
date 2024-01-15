# live_chat/views.py
from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import ChatMessage, ChatRoom
from .serializers import ChatRoomSerializer, ChatMessageSerializer

def live_chat(request):
    return render(request, 'chat/live_chat.html', {})


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_messages(request, room_id):
#     try:
#         messages = ChatMessage.objects.filter(room__id=room_id)
#         serializer = ChatMessageSerializer(messages, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_chat_message(request, room_name):
    try:
        user = request.user
        message = request.data.get('message', '')

        if not message:
            return Response({'error': 'Content is required.'}, status=status.HTTP_400_BAD_REQUEST)

        room = ChatRoom.objects.get(room_name=room_name)
        message = ChatMessage.objects.create(room=room, user=user, message=message)

        serializer = ChatMessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ChatRoomListView(generics.ListAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer

class ChatMessageListView(generics.ListCreateAPIView):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
