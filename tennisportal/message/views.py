from rest_framework import status
from rest_framework.response import Response
from .serializers import MessageSerializer
from .models import Message
from django.db.models import Q
from rest_framework.decorators import api_view


@api_view(['POST', 'GET', 'PUT'])
def message_service(request):
    if request.method == 'POST':
        try:
            if request.data.get('message_from').get('id') == request.user.id:
                message = MessageSerializer(data=request.data)
                if message.is_valid():
                    message.save()
                    return Response(message.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(message.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(
                    {'error_messages': {'messages': ["Operation disallowed."]}},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        except AttributeError:
            return Response(
                {'error_messages': {'messages': ["Message addressee is missing."]}},
                status=status.HTTP_400_BAD_REQUEST
            )
        except KeyError as key_error:
            return Response(
                {'error_messages': {'messages': ["Following fields are missing: " + str(key_error) + "."]}},
                status=status.HTTP_400_BAD_REQUEST
            )
    elif request.method == 'GET':
        all_messages = Message.objects.filter(
            Q(message_from=request.user) | Q(message_to=request.user)
        ).order_by('sent').distinct()

        serializer = MessageSerializer(all_messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        messages = []
        if request.data.get('messages') is not None:
            for message_id in request.data.get('messages'):
                try:
                    message = Message.objects.get(message_id=message_id, message_to=request.user)
                    message.received = True
                    message.save()
                    messages.append(message)
                except Message.DoesNotExist:
                    continue
            serializer = MessageSerializer(messages, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error_messages': {'messages': ["Messages list is missing."]}},
                status=status.HTTP_400_BAD_REQUEST
            )


