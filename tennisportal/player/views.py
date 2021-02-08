from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from player.serializers import PlayerSerializer
from .models import Player
from django.db.models import Q
from rest_framework.permissions import AllowAny
from datetime import date
from django.db.utils import IntegrityError


def build_player_data(player):
    return {
        'id': player.id,
        'email': player.email,
        'username': player.username,
        'first_name': player.first_name,
        'last_name': player.last_name,
        'gender': player.gender,
        'weight': player.weight,
        'height': player.height,
        'ntrp': player.ntrp,
        'plays': player.plays,
        'backhand': player.backhand,
        'birthdate': player.birthdate,
        'auth_token': Token.objects.get(user=player).key
    }


def subtract_years(years):
    today = date.today()
    return date(today.year - int(years), today.month, today.day)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def register(request):
    try:
        if request.data.get('password1') == request.data.get('password2'):
            serializer = PlayerSerializer(data=request.data)
            if serializer.is_valid():
                new_player = serializer.save()
                Token.objects.create(user=new_player)
                new_player.set_password(request.data.get('password1'))
                new_player.save()
                new_player_data = build_player_data(new_player)
                return Response(new_player_data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {'error_messages': {"password": ["Passwords are not the same."]}},
                status=status.HTTP_400_BAD_REQUEST,
            )
    except IntegrityError:
        return Response(
            {'error_messages': {"account": ["Username or email already taken."]}},
            status=status.HTTP_409_CONFLICT
        )


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def login(request):
    player = authenticate(username=request.data.get('email'), password=request.data.get('password'))
    if player is not None:
        Token.objects.create(user=player)
        return Response(build_player_data(player), status=status.HTTP_200_OK)
    else:
        return Response(
            {'error_messages': {"login": ['Wrong email or password']}},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['DELETE'])
def logout(request):
    try:
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({'message': 'Logout successful.'}, status=status.HTTP_200_OK)
    except Token.DoesNotExist:
        return Response({'error_messages': {'logout': ['User is not logged in.']}}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['PUT', 'DELETE', 'GET'])
def players_service(request):
    if request.method == 'PUT':
        if request.data:
            try:
                player = Player.objects.get(id=request.user.id)
                serializer = PlayerSerializer(player, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Player.DoesNotExist:
                return Response(
                    {'error_messages': {'players': ["Account doesn't exist"]}},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response({'error_messages': {'players': ["Empty request"]}}, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        try:
            print(request.data)
            if request.data.get('password1') == request.data.get('password2'):
                player = authenticate(username=request.user.email, password=request.data.get('password1'))
                print(player)
                if player is not None:
                    player.delete()
                    return Response({'response': 'Account has been deleted.'}, status=status.HTTP_200_OK)
                else:
                    return Response(
                        {'error_messages': {'players': ["Account you are trying to delete does not exist."]}},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {'error_messages': {'players': ["Passwords are not the same"]}},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Player.DoesNotExist:
            return Response(
                {'error_messages': {'players': ["Account you are trying to delete does not exist"]}},
                status=status.HTTP_400_BAD_REQUEST
            )
    elif request.method == 'GET':
        if len([value for value in request.query_params.values()]) > 0:
            try:
                name = request.query_params.get('name')
                max_ntrp = request.query_params.get('max_ntrp')
                min_ntrp = request.query_params.get('min_ntrp')
                max_age = request.query_params.get('max_age')
                min_age = request.query_params.get('min_age')
                gender = request.query_params.get('gender')

                players = Player.objects.all()
                if name is not None:
                    players = players.filter(
                        Q(username__contains=name) | Q(first_name__contains=name) | Q(last_name__contains=name)
                    )
                if gender is not None:
                    players = players.filter(gender=gender)
                if max_ntrp is not None:
                    players = players.filter(ntrp__lte=max_ntrp)
                if min_ntrp is not None:
                    players = players.filter(ntrp__gte=min_ntrp)
                if max_age is not None:
                    birthdate = subtract_years(max_age)
                    players = players.filter(birthdate__gte=birthdate)
                if min_age is not None:
                    birthdate = subtract_years(min_age)
                    players = players.filter(birthdate__lte=birthdate)

                players = players.distinct().exclude(id=request.user.id).order_by('username')
                serializer = PlayerSerializer(players, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ValueError:
                return Response(
                    {'error_messages': {'players': ["Wrong data type provided."]}},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            serializer = PlayerSerializer(request.user, many=False)
            return Response(serializer.data,
                            status=status.HTTP_200_OK)


@api_view(['PUT'])
def update_password(request):
    if request.data.get('new_password1') == request.data.get('new_password2'):
        try:
            account = authenticate(username=request.user.email, password=request.data.get('password'))
            account.set_password(request.data.get('new_password1'))
            account.save()
            return Response({'message': 'Password updated.'}, status=status.HTTP_200_OK)
        except Player.DoesNotExist:
            return Response(
                {'error_messages': {'account': ['Account does not exist']}},
                status=status.HTTP_400_BAD_REQUEST
            )
    else:
        return Response(
            {'error_messages': {'passwords': ["Passwords don't match"]}},
            status=status.HTTP_400_BAD_REQUEST
        )
