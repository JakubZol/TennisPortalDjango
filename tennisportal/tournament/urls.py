from django.urls import path
from .views import get_owned_tournaments, tournaments_service, entries_service

app_name = 'tournament'

urlpatterns = [
    path('', tournaments_service, name='tournaments'),
    path('/owned/', get_owned_tournaments, name='get owned tournaments'),
    path('/entries', entries_service, name='entries')
]
