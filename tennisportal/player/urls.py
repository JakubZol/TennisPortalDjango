from django.urls import path
from player.views import register, login, logout, players_service, update_password

app_name = 'player'

urlpatterns = [
    path('/register', register, name='register'),
    path('/login', login, name='login'),
    path('/logout', logout, name='logout'),
    path('', players_service, name='modify account'),
    path('/password', update_password, name='update password')
]
