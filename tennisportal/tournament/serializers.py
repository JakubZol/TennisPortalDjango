from rest_framework import serializers
from .models import Tournament, Entry
from player.serializers import PlayerSerializer
from player.models import Player
from match.models import Match


class EntryTournamentSerializer(serializers.ModelSerializer):
    owner = PlayerSerializer()

    class Meta:
        model = Tournament
        fields = ['tournament_id', 'owner', 'tournament_name', 'rounds_number', 'prize_money', 'prize_currency',
                  'finished', 'cancelled']


class EntrySerializer(serializers.ModelSerializer):
    player = PlayerSerializer(required=True)
    tournament = EntryTournamentSerializer(required=True)

    class Meta:
        model = Entry
        fields = ['tournament', 'player', 'seed', 'accepted']

    def run_validation(self, data=None):
        return data

    def create(self, validated_data):
        tournament = Tournament.objects.get(tournament_id=validated_data.pop('tournament')['tournament_id'])
        player = Player.objects.get(username=validated_data.pop('player')['username'])
        seed = validated_data.get('seed') if validated_data.get('seed') is not None else None
        return Entry.objects.create(
            tournament=tournament,
            player=player,
            seed=seed,
            accepted=(tournament.owner.id == player.id)
        )

    def update(self, instance, validated_data):
        instance.seed = validated_data.get('seed', instance.seed)
        instance.accepted = validated_data.get('seed', instance.accepted)

        return instance


class TournamentEntrySerializer(serializers.ModelSerializer):
    player = PlayerSerializer(required=True)

    class Meta:
        model = Entry
        fields = ['player', 'seed', 'accepted']


class TournamentMatchSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True)
    opponents = PlayerSerializer(many=True)

    class Meta:
        model = Match
        fields = ['match_id', 'players', 'opponents', 'score', 'date', 'round']


class TournamentSerializer(serializers.ModelSerializer):
    owner = PlayerSerializer(required=True)
    winners = PlayerSerializer(many=True, required=False, default=[])
    entry = TournamentEntrySerializer(source='entry_set', many=True, required=False, default=[], read_only=True)
    matches = TournamentMatchSerializer(source='match_set', many=True, required=False, default=[], read_only=True)

    class Meta:
        model = Tournament
        fields = ['tournament_id', 'tournament_name', 'owner', 'rounds_number', 'prize_money', 'prize_currency', 'finished', 'cancelled', 'winners', 'entry', 'matches']

    def create(self, validated_data):
        owner = Player.objects.get(username=validated_data.pop('owner')['username'])

        return Tournament.objects.create(
            tournament_name=validated_data.pop('tournament_name'),
            owner=owner,
            rounds_number=validated_data.pop('rounds_number'),
            prize_money=validated_data.pop('prize_money'),
            prize_currency=validated_data.pop('prize_currency'),
        )
