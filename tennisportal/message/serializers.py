from rest_framework import serializers
from .models import Message
from player.serializers import PlayerSerializer
from player.models import Player


class MessageSerializer(serializers.ModelSerializer):
    message_from = PlayerSerializer(many=False)
    message_to = PlayerSerializer(many=False)

    class Meta:
        model = Message
        fields = ['message_id', 'message_from', 'message_to', 'message', 'sent', 'received']

    def create(self, validated_data):
        message_from = validated_data.pop('message_from')
        message_to = validated_data.pop('message_to')
        return Message.objects.create(
            message_to=Player.objects.get(username=message_to['username']),
            message_from=Player.objects.get(username=message_from['username']),
            message=validated_data.pop('message')
        )

