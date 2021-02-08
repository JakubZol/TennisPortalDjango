from django.db import models


class Match(models.Model):
    match_id = models.AutoField(primary_key=True)
    players = models.ManyToManyField('player.Player', null=False, related_name='players')
    opponents = models.ManyToManyField('player.Player', null=False, related_name='opponents')
    score = models.CharField(max_length=20, null=True, blank=True)
    date = models.DateField()
    tournament = models.ForeignKey(
        'tournament.Tournament',
        models.SET_NULL,
        null=True,
        blank=True,
    )
    round = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return 'Match ' + str(self.match_id) + ', score: ' + self.score
