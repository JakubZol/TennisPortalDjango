from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('players', include('player.urls')),
    path('messages', include('message.urls')),
    path('matches', include('match.urls')),
    path('tournaments', include('tournament.urls')),
]
