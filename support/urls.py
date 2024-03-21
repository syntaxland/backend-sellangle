# support/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create-support-ticket/', views.user_create_support_ticket, name='create-support-ticket'),

    path('list-support-ticket/', views.list_support_ticket, name='list-support-ticket'),
    path('get-ticket-detail/<int:ticket_id>/', views.get_ticket_detail, name='get-ticket-reply-detail'),

    path('user-reply-support-ticket/', views.user_reply_support_ticket, name='reply-support-ticket'),
    path('admin-reply-support-ticket/', views.admin_reply_support_ticket, name='admin-user-reply-support-ticket'),
    path('list-support-ticket-reply/<int:ticket_id>/', views.list_support_ticket_reply, name='list-support-ticket-reply'),

    path('list-all-support-ticket/', views.list_all_support_ticket, name='list-all-support-ticket'),
    path('list-all-support-response/', views.list_all_support_response, name='list-all-support-response'), 

    path('clear-user-support-message-counter/', views.clear_user_support_message_counter, name='clear_user_support_message_counter'), 
    path('clear-admin-support-message-counter/', views.clear_admin_support_message_counter, name='clear_admin_support_message_counter'), 

]
 