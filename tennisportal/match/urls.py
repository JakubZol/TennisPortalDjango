from django.urls import path
from .views import matches_service

app_name = 'match'

urlpatterns = [
    path('', matches_service),
]
