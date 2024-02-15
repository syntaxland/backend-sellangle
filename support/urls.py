# support/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create-support-ticket/', views.create_support_ticket, name='create-support-ticket'),

    path('list-support-ticket/', views.list_support_ticket, name='list-support-ticket'),
    path('get-ticket-detail/<int:ticket_id>/', views.get_ticket_detail, name='get-ticket-reply-detail'),

    path('reply-support-ticket/', views.reply_support_ticket, name='reply-support-ticket'),
    path('list-support-ticket-reply/<int:ticket_id>/', views.list_support_ticket_reply, name='list-support-ticket-reply'),

    path('list-all-support-ticket/', views.list_all_support_ticket, name='list-all-support-ticket'),
    path('list-all-support-response/', views.list_all_support_response, name='list-all-support-response'), 
]
 