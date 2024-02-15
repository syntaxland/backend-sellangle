# feedback/views.py
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Feedback
from .serializers import FeedbackSerializer

from django.contrib.auth import get_user_model

User = get_user_model()


@api_view(['POST']) 
@permission_classes([IsAuthenticated]) 
def create_feedback(request):
    user=request.user
    data=request.data

    category=data['category']
    subject=data['subject']
    message=data['message']
    print('category:', category, 'subject:', subject)
    
    Feedback.objects.create(
            user=user,  
            category=category,
            subject=subject,
            message=message,
        )
    return Response({'message': 'Feedback created.'}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def list_feedback(request):
    # user = request.user
    try:
        # feedback = SupportTicket.objects.filter(user=user).order_by('-created_at')
        feedback = Feedback.objects.all()
        serializer = FeedbackSerializer(feedback, many=True)
        return Response(serializer.data)
    except Feedback.DoesNotExist:
        return Response({'detail': 'Feedback not found'}, status=status.HTTP_404_NOT_FOUND)
