# support/views.py
import random
import string

from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import SupportTicket, SupportResponse
from .serializers import SupportTicketSerializer, SupportResponseSerializer

from .tasks import check_support_is_expired

from django.shortcuts import get_object_or_404 
from django.http.response import HttpResponse
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

User = get_user_model()

def generate_ticket_id():
    return ''.join(random.choices(string.digits, k=9))


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def create_support_ticket(request):
#     user=request.user
#     data=request.data

#     serializer = SupportTicketSerializer(data=data)

#     if serializer.is_valid():
#         ticket_id = generate_ticket_id()
#         serializer.save(user=user, ticket_id=ticket_id)

#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def create_support_ticket(request):
    user=request.user
    data=request.data

    category=data['category']
    subject=data['subject']
    message=data['message']
    ticket_id = generate_ticket_id()
    print('category:', category, 'subject:', subject)
    
    SupportTicket.objects.create(
            user=user, 
            category=category,
            subject=subject,
            message=message,
            ticket_id=ticket_id,
        )
    return Response({'message': 'Support ticket created.'}, status=status.HTTP_201_CREATED)


# @api_view(['POST'])
# # @permission_classes([IsAuthenticated])
# def create_support_message(request):
#     # user=request.user
#     data=request.data
#     ticket_id = generate_ticket_id()

#     serializer = SupportMessageSerializer(data=data)

#     if serializer.is_valid():

#         support_ticket = SupportTicket.objects.create(
#             # user=user, 
#             ticket_id = ticket_id,
#         )
#         serializer.save(
#             # user=user, 
#             support_ticket=support_ticket
#         )

#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reply_support_ticket(request):
    user=request.user
    data=request.data

    ticket_id=data['ticket_id']
    print('ticket_id:', ticket_id)
    message=data['message']
    print('message:', message)
    
    try:
        support_ticket = SupportTicket.objects.get(
            ticket_id=ticket_id)
    except SupportTicket.DoesNotExist:
        return Response({'detail': 'Support ticket not found'}, status=status.HTTP_404_NOT_FOUND)
    
    SupportResponse.objects.create(
            user=user, 
            support_ticket=support_ticket,
            message=message,
        )
    return Response({'message': 'Support ticket replied'}, status=status.HTTP_201_CREATED)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_support_ticket(request):
    user=request.user
    data=request.data

    try:
        support_ticket = SupportTicket.objects.filter(user=user, 
                                                      ).order_by('-created_at')
        serializer = SupportTicketSerializer(support_ticket, many=True)
        return Response(serializer.data)
    except SupportTicket.DoesNotExist:
        return Response({'detail': 'Support ticket not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_support_ticket_reply(request, ticket_id):
    user = request.user
    print('ticket_id:', ticket_id)

    try:
        support_ticket = SupportTicket.objects.get(
            ticket_id=ticket_id
            )
    except SupportTicket.DoesNotExist:
        return Response({'detail': 'Support ticket not found'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        support_reply = SupportResponse.objects.filter(
            # user=user,
            support_ticket=support_ticket,
            ).order_by('created_at')
        serializer = SupportResponseSerializer(support_reply, many=True)
        return Response(serializer.data)
    except SupportResponse.DoesNotExist:
        return Response({'detail': 'support reply not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_all_support_ticket(request):
    try:
        support_ticket = SupportTicket.objects.all().order_by('-created_at')
        serializer = SupportTicketSerializer(support_ticket, many=True)
        return Response(serializer.data)
    except SupportTicket.DoesNotExist:
        return Response({'detail': 'support tickets not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_all_support_response(request):
    try:
        responses = SupportResponse.objects.all().order_by('created_at')
        serializer = SupportResponseSerializer(responses, many=True)
        return Response(serializer.data)
    except SupportResponse.DoesNotExist:
        return Response({'detail': 'support responses not found'}, status=status.HTTP_404_NOT_FOUND)
    

def trigger_check_support_is_expired(request):
    if check_support_is_expired:
        result = check_support_is_expired.delay()
        return HttpResponse({'task_id': result.id})
    return HttpResponse({'message': 'Invalid request method'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_ticket_detail(request, ticket_id):
    user=request.user
    print('ticket_id:', ticket_id)
    try:
        support_ticket = SupportTicket.objects.filter(
            # user=user, 
            ticket_id=ticket_id,
            ).order_by('-created_at')
        serializer = SupportTicketSerializer(support_ticket, many=True)
        return Response(serializer.data)
    except SupportTicket.DoesNotExist:
        return Response({'detail': 'Support ticket not found'}, status=status.HTTP_404_NOT_FOUND)
