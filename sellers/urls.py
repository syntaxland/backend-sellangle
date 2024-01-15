from django.urls import path
from . import views

urlpatterns = [
    path('celery-test', views.test, name="test"),
    # path('sendmail/', views.send_mail_to_all, name="sendmail"),
    # path('schedulemail/', views.schedule_mail, name="schedulemail"),
]
