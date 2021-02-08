from rest_framework import serializers
from .models import Match
from player.serializers import PlayerSerializer
from player.models import Player
from tournament.models import Tournament
from django.db.models import Q
from tournament.serializers import EntryTournamentSerializer


class MatchSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True)
    opponents = PlayerSerializer(many=True)
    tournament = EntryTournamentSerializer(many=False, required=False)

    class Meta:
        model = Match
        fields = ['match_id', 'players', 'opponents', 'score', 'date', 'tournament', 'round']

    def run_validation(self, data=None):
        return data

    def create(self, validated_data):
        tournament = validated_data.get('tournament', None)
        if tournament is not None:
            tournament = Tournament.objects.get(tournament_id=tournament.get('tournament_id'))

        new_match = Match.objects.create(
            score=validated_data.get('score'),
            date=validated_data.get('date'),
            tournament=tournament,
            round=validated_data.get('round', None),
        )

        players = map(lambda player: player.get('id'), validated_data.get('players'))
        opponents = map(lambda player: player.get('id'), validated_data.get('opponents'))

        new_match.players.set(players)
        new_match.opponents.set(opponents)

        return new_match





