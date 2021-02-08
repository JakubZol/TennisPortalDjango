from django.db import models
from django.utils import timezone


class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    message_from = models.ForeignKey('player.Player', models.CASCADE, related_name='message_from')
    message_to = models.ForeignKey('player.Player', models.CASCADE, related_name='message_to')
    message = models.TextField(default='')
    sent = models.DateTimeField(default=timezone.now())
    received = models.BooleanField(default=False)

    def __str__(self):
        return 'Message: ' + str(self.message_id) + str(self.message)
