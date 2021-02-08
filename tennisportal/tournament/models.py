from django.db import models


class Tournament(models.Model):
    tournament_id = models.AutoField(primary_key=True)
    tournament_name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        'player.Player',
        models.SET_NULL,
        null=True,
        related_name='tournament_owner'
    )
    rounds_number = models.IntegerField()
    prize_money = models.IntegerField(blank=True, null=True)
    prize_currency = models.CharField(max_length=3, blank=True, null=True)
    finished = models.BooleanField(default=False)
    cancelled = models.BooleanField(default=False)
    winners = models.ManyToManyField('player.Player', null=True, blank=True, default=None, related_name='tournament_winners')

    def __str__(self):
        return 'Tournament ' + str(self.tournament_name) + ': ' + self.tournament_name


class Entry(models.Model):
    tournament = models.ForeignKey(
        'tournament',
        models.CASCADE,
        null=False,
    )
    player = models.ForeignKey(
        'player.Player',
        models.SET_NULL,
        null=True,
    )
    seed = models.IntegerField(blank=True, null=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return 'Entry for ' + str(self.player) + '(' + str(self.seed) + ')'

