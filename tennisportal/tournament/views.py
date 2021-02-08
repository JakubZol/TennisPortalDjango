from rest_framework import status
from rest_framework.response import Response
from .models import Tournament, Entry
from .serializers import TournamentSerializer, EntrySerializer
from player.models import Player
from django.db.models import Q, Count, F
from rest_framework.decorators import api_view


@api_view(['GET'])
def get_owned_tournaments(request):
    try:
        owned_tournaments = Tournament.objects.filter(owner=request.user)
        serializer = TournamentSerializer(owned_tournaments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Player.DoesNotExist:
        return Response({'error_messages': {'owner': ['Account does not exist.']}}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'DELETE', 'PUT', 'GET'])
def tournaments_service(request):
    if request.method == 'POST':
        try:
            if request.data.get('owner').get('id') == request.user.id:
                tournament = TournamentSerializer(data=request.data, many=False)
                if tournament.is_valid():
                    tournament.save()
                    return Response(tournament.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(tournament.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(
                    {'error_messages': {'tournaments': ["Operation disallowed."]}},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        except (AttributeError, KeyError) as e:
            return Response(
                    {'error_messages': {'tournaments': ["Required data is missing."]}},
                    status=status.HTTP_400_BAD_REQUEST
                )
    elif request.method == 'PUT':
        try:
            tournament = Tournament.objects.get(tournament_id=request.data['tournament_id'], owner=request.user)
            serializer = TournamentSerializer(tournament, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Tournament.DoesNotExist:
            return Response(
                {'error_messages': {'tournament': ["Tournament doesn't exist."]}},
                status=status.HTTP_400_BAD_REQUEST
            )
        except AssertionError:
            return Response(
                {'error_messages': {'tournament': ["Some fields are forbidden to modify."]}},
                status=status.HTTP_400_BAD_REQUEST
            )
    elif request.method == 'DELETE':
        try:
            tournament = Tournament.objects.get(tournament_id=request.data['tournament_id'], owner=request.user)
            tournament.delete()
            return Response({'message': 'Tournament deleted.'}, status=status.HTTP_200_OK)
        except Tournament.DoesNotExist:
            return Response(
                {'error_messages': {'tournament': ["Tournament doesn't exist."]}},
                status=status.HTTP_400_BAD_REQUEST
            )
        except KeyError:
            return Response(
                {'error_messages': {'tournament': ["No valid data provided."]}},
                status=status.HTTP_400_BAD_REQUEST
            )
    elif request.method == 'GET':
        if len([value for value in request.query_params.values()]) == 0:
            try:
                tournaments = Tournament.objects.filter(entry__player=request.user).exclude(owner=request.user).distinct()
                serializer = TournamentSerializer(tournaments, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

            except Player.DoesNotExist:
                return Response({'error_messages': {'player': ['Player does not exist.']}},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            tournament_name = request.query_params.get('tournament_name')
            min_prize_money = request.query_params.get('min_prize_money')
            max_prize_money = request.query_params.get('max_prize_money')
            max_rounds = request.query_params.get('max_rounds')
            min_rounds = request.query_params.get('min_rounds')
            prize_currency = request.query_params.get('prize_currency')
            finished = request.query_params.get('finished')
            cancelled = request.query_params.get('cancelled')
            entry_available = request.query_params.get('entry_available')

            tournaments = Tournament.objects.all()
            if tournament_name is not None:
                tournaments = tournaments.filter(tournament_name__contains=tournament_name)
            if prize_currency is not None:
                tournaments = tournaments.filter(prize_currency=prize_currency)
                if min_prize_money is not None:
                    tournaments = tournaments.filter(prize_money__gte=min_prize_money)
                if max_prize_money is not None:
                    tournaments = tournaments.filter(prize_money__lte=max_prize_money)
            if finished is not None:
                tournaments = tournaments.filter(finished=finished)
            if cancelled is not None:
                tournaments = tournaments.filter(cancelled=cancelled)
            if max_rounds is not None:
                tournaments = tournaments.filter(rounds_number__lte=max_rounds)
            if min_rounds is not None:
                tournaments = tournaments.filter(rounds_number__gte=min_rounds)
            if entry_available is not None:
                if entry_available:
                    tournaments = tournaments. \
                        annotate(entries_count=Count('entry')). \
                        filter(cancelled=False, finished=False, entries_count__lt=(pow(2, F('rounds_number'))))
                else:
                    tournaments = tournaments. \
                        annotate(entries_count=Count('entry')). \
                        filter(Q(cancelled=False) | Q(finished=False) | Q(entries_count=(pow(2, F('rounds_number')))))
            print(tournaments)

            serializer = TournamentSerializer(tournaments.distinct(), many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST', 'DELETE', 'PUT', 'GET'])
def entries_service(request):
    if request.method == 'POST':
        if request.data.get('tournament').get('owner').get('id') == request.user.id:
            entry = EntrySerializer(data=request.data, many=False)
            if entry.is_valid():
                entry.save()
                return Response(entry.data, status=status.HTTP_201_CREATED)
            else:
                return Response(entry.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {'error_messages': {'entries': ["Operation disallowed."]}},
                status=status.HTTP_400_BAD_REQUEST
            )
    elif request.method == 'DELETE':
        try:
            entry = Entry.objects.get(
                player=request.user,
                tournament__tournament_id=request.data.get('tournament')['tournament_id']
            )
            entry.delete()
            return Response({'message': 'Invitation to the tournament declined.'}, status=status.HTTP_200_OK)
        except Entry.DoesNotExist:
            return Response(
                {'error_messages': {'entry': ['No active invitation to the tournament.']}},
                status=status.HTTP_400_BAD_REQUEST
            )
    elif request.method == 'PUT':
        try:
            print(request.data)
            entry = Entry.objects.get(
                player=request.user,
                tournament=request.data.get('tournament')['tournament_id']
            )
            entry.accepted = request.data.get('accepted', entry.accepted)
            entry.save()
            serializer = EntrySerializer(entry, many=False)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Entry.DoesNotExist:
            return Response(
                {'error_messages': {'entry': ["Tournament doesn't exist."]}},
                status=status.HTTP_400_BAD_REQUEST
            )
