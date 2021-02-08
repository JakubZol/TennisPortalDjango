from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q
from .serializers import MatchSerializer
from player.models import Player
from .models import Match
from rest_framework.decorators import api_view


@api_view(['POST', 'GET', 'DELETE', 'PUT'])
def matches_service(request):
    if request.method == 'GET':
        try:
            player_matches = Match.objects.filter(Q(players=request.user) | Q(opponents=request.user)).order_by('date').distinct()
            serializer = MatchSerializer(player_matches, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Player.DoesNotExist:
            return Response({'error_messages': {'matches': ['Player does not exist.']}})
    elif request.method == 'POST':
        players_ids = map(lambda player: player.get('id'), request.data.get('players'))
        opponents_ids = map(lambda player: player.get('id'), request.data.get('opponents'))
        if request.user.id in players_ids or request.user.id in opponents_ids:
            match = MatchSerializer(data=request.data)
            if match.is_valid():
                match.save()
                return Response(match.data, status=status.HTTP_201_CREATED)
            else:
                return Response(match.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {'error_messages': {'matches': ["Operation disallowed."]}},
                status=status.HTTP_401_UNAUTHORIZED
            )
    elif request.method == 'DELETE':
        try:
            match = Match.objects.filter(
                Q(match_id=request.data.get('match_id')),
                Q(players=request.user) | Q(opponents=request.user),
            ).distinct().first()
            if match.tournament is None or match.tournament.owner == request.user:
                match.delete()
                return Response({'message': 'Match deleted.'}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {'error_messages': {'match': ['This match is a part of a tournament. You can not delete it.']}},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        except Match.DoesNotExist:
            return Response(
                {'error_messages': {'match': ['Match does not exist.']}},
                status=status.HTTP_400_BAD_REQUEST
            )
        except AttributeError:
            return Response(
                {'error_messages': {'match': ['Match does not exist or you have no rights to delete it.']}},
                status=status.HTTP_400_BAD_REQUEST
            )
    elif request.method == 'PUT':
        try:
            match = Match.objects.get(match_id=request.data.get('match_id'))
            match.date = request.data.get('date', match.date)
            match.score = request.data.get('score', match.score)
            match.save()
            serializer = MatchSerializer(match, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Player.DoesNotExist:
            return Response({'error_messages': {'matches': ['Player does not exist.']}})
