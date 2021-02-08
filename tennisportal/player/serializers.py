from rest_framework import serializers
from .models import Player


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'gender', "height", "weight", 'ntrp', 'plays', 'backhand', 'birthdate']
        extra_kwargs = {
            'email': {'validators': []},
            'username': {'validators': []},
            'id': {'validators': []}
        }



