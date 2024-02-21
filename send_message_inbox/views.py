from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from rest_framework import status, generics
from rest_framework.views import APIView

from .serializers import SendMessageInboxSerializer   
from .models import  SendMessageInbox

from django.shortcuts import get_object_or_404
from django.db.models import Sum, F
from django.contrib.auth import get_user_model

User = get_user_model() 


@api_view(['POST'])
@permission_classes([IsAuthenticated])  
def send_message_to_all(request):
    user = request.user
    receivers = User.objects.all()

    subject = request.data.get('subject')
    message = request.data.get('message')
    print('receivers:',receivers)
    print('subject:',subject)
    
    for receiver in receivers:
        inbox = SendMessageInbox.objects.create(
            sender=user,
            receiver=receiver,
            subject=subject,
            message=message
        )

        inbox.msg_count += 1
        inbox.save()

    return Response({'message': 'Messages sent.'}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def message_inbox_view(request):
    try:
        message_inbox = SendMessageInbox.objects.all().order_by('-timestamp')
        serializer = SendMessageInboxSerializer(message_inbox, many=True)
        return Response(serializer.data)
    except SendMessageInbox.DoesNotExist:
        return Response({'detail': 'Messages not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_message_inbox(request):
    user = request.user
    try:
        message_inbox = SendMessageInbox.objects.filter(receiver=user).order_by('-timestamp')
        serializer = SendMessageInboxSerializer(message_inbox, many=True)
        return Response(serializer.data)
    except SendMessageInbox.DoesNotExist:
        return Response({'detail': 'Messages not found'}, status=status.HTTP_404_NOT_FOUND)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_message_count(request):
#     user = request.user
#     msg_count = SendMessageInbox.objects.filter(receiver=user).aggregate(Sum('msg_count'))['msg_count__sum'] or 0
#     return Response({'msg_count': msg_count}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def clear_message_counter(request):
    user = request.user
    data = request.data
    print('data:', data, 'user:', user)

    msg_id = data.get('msg_id')
    print('msg_id:', msg_id)

    try:
        mesg_inbox = SendMessageInbox.objects.get(receiver=user, id=msg_id)
    except SendMessageInbox.DoesNotExist:
        return Response({'detail': 'Promise message not found'}, status=status.HTTP_404_NOT_FOUND)

    if mesg_inbox.msg_count > 0:
        mesg_inbox.msg_count -= 1

    mesg_inbox.is_read = True
    mesg_inbox.save()

    return Response({'message': 'Message cleared.'}, status=status.HTTP_200_OK)
