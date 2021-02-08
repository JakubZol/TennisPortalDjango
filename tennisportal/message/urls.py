from django.urls import path
from message.views import message_service

app_name = 'message'

urlpatterns = [
    path('', message_service, name='message'),
]
