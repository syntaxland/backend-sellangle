# support/views.py
import random
import string

from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import SupportTicket, SupportResponse
from .serializers import SupportTicketSerializer, SupportResponseSerializer 
from send_email.send_email_sendinblue import send_email_sendinblue
from django.conf import settings
from django.shortcuts import get_object_or_404 
from django.http.response import HttpResponse
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

User = get_user_model()

def generate_ticket_id():
    return ''.join(random.choices(string.digits, k=16))


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_create_support_ticket(request):
    user = request.user
    data = request.data

    category = data['category']
    subject = data['subject']
    message = data['message']
    ticket_id = generate_ticket_id()

    ticket = SupportTicket.objects.create(
        user=user,
        category=category,
        subject=subject,
        message=message,
        ticket_id=ticket_id,
    )

    if ticket:
        ticket.admin_user_msg_count += 1
        ticket.modified_at = timezone.now()
        ticket.save()

    # Send an email to notify the user that their support ticket is opened
    subject = f"Your support ticket #{ticket_id} is now open"
    first_name = user.first_name if user.first_name else 'User'
    url = settings.SELLANGLE_URL
    support_url = f"{url}/support/ticket/{ticket_id}"
    html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Support Ticket Opened</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                }}
                .header {{
                    background-color: #4CAF50;
                    color: white;
                    padding: 1em;
                    text-align: center;
                }}
                .content {{
                    padding: 1em;
                }}
                .footer {{
                    background-color: #f1f1f1;
                    padding: 1em;
                    text-align: center;
                }}
                .button {{
                    display: inline-block;
                    background-color: #2196f3;
                    color: #fff;
                    padding: 10px 20px;
                    text-decoration: none;
                    border-radius: 5px; /* Rounded corners */
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>Support Ticket Opened</h2>
                </div>
                <div class="content">
                    <p>Dear {first_name.title()},</p>
                    <p>Your support ticket with <b>Ticket ID: #{ticket_id}</b> has been opened. 
                    If you have any questions or need assistance, please feel free to reach out to us. 
                    You can also reply to this email or use the following link to view and update your support ticket:</p>
                    <p><a href="{support_url}" class="button">View/Update Ticket</a></p>
                    <p>Best regards,</p>
                    <p>Your Support Team</p>
                </div>
                <div class="footer">
                    <p><em>This email was sent from an address that cannot accept incoming emails. 
                    Please use the link above if you need to contact us about this same issue.</em></p>
                    <p><em>{settings.COMPANY_NAME} is a subsidiary and registered trademark of {settings.PARENT_COMPANY_NAME}.</em></p>
                </div>
            </div>
        </body>
        </html>
    """

    to = [{"email": user.email, "name": user.first_name}]
    send_email_sendinblue(subject, html_content, to)

    return Response({'message': 'Support ticket created.'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_reply_support_ticket(request):
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
    
    if support_ticket:
        support_ticket.admin_user_msg_count += 1
        # support_ticket.message = message
        support_ticket.is_closed = False
        support_ticket.is_resolved = False
        support_ticket.modified_at = timezone.now()
        support_ticket.save()
    return Response({'message': 'Support ticket replied'}, status=status.HTTP_201_CREATED)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_reply_support_ticket(request):
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
    
    if support_ticket:
        support_ticket.user_msg_count += 1
        # support_ticket.message = message
        support_ticket.is_closed = False
        support_ticket.is_resolved = False
        support_ticket.modified_at = timezone.now()
        support_ticket.save()
    return Response({'message': 'Support ticket replied'}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_support_ticket(request):
    user=request.user
    data=request.data

    try:
        support_ticket = SupportTicket.objects.filter(user=user, 
                                                      ).order_by('modified_at')
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
        support_ticket = SupportTicket.objects.all().order_by('modified_at')
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



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def clear_user_support_message_counter(request):
    user = request.user
    data = request.data
    print('data:', data, 'user:', user)

    ticket_id = data.get('ticket_id')
    print('ticket_id:', ticket_id)

    try:
        ticket = SupportTicket.objects.get(ticket_id=ticket_id)
    except SupportTicket.DoesNotExist:
        return Response({'detail': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if ticket.user_msg_count > 0:
        ticket.user_msg_count = 0
        ticket.save()
        print('user_msg_count (cleared):', ticket.user_msg_count)

    return Response({'message': 'Message cleared.'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def clear_admin_support_message_counter(request):
    user = request.user
    data = request.data
    print('data:', data, 'user:', user)

    ticket_id = data.get('ticket_id')
    print('ticket_id:', ticket_id)

    try:
        ticket = SupportTicket.objects.get(ticket_id=ticket_id)
    except SupportTicket.DoesNotExist:
        return Response({'detail': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)

    if ticket.admin_user_msg_count > 0:
        ticket.admin_user_msg_count = 0
        ticket.save()
        print('admin_user_msg_count (cleared):', ticket.admin_user_msg_count)

    return Response({'message': 'Message cleared.'}, status=status.HTTP_200_OK)
