from django.conf import settings
from django.db import models, transaction


class Match(models.Model):
    class MatchType(models.IntegerChoices):
        BO1 = 1, 'Best of 1'
        BO3 = 3, 'Best of 3'
        BO5 = 5, 'Best of 5'
    
    requesting_player = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='matches', on_delete=models.CASCADE)
    confirming_player = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='_matches', on_delete=models.CASCADE)
    result = models.BooleanField()
    is_confirmed = models.BooleanField(default=False)
    elo_change = models.SmallIntegerField()
    match_type = models.PositiveSmallIntegerField(choices=MatchType.choices)

    @property
    def winner(self):
        return self.requesting_player if self.result else self.confirming_player

    @property
    def loser(self):
        return self.confirming_player if self.result else self.requesting_player

    def confirm(self):
        self.is_confirmed = True
        requesting_player = self.requesting_player
        confirming_player = self.confirming_player
        requesting_player.elo += self.elo_change
        confirming_player.elo -= self.elo_change
        with transaction.Atomic():
            requesting_player.save()
            confirming_player.save()
            self.save()

    def calculate_elo_change(self):
        r_a = self.requesting_player.elo
        r_b = self.confirming_player.elo
        K = 40
        self.elo_change = K / (1 + 10 ** ((r_a - r_b) / 400))
        


class Game(models.Model):
    match = models.ForeignKey(Match, related_name='games', on_delete=models.CASCADE)
    requesting_player_score = models.PositiveSmallIntegerField()
    confirming_player_score = models.PositiveSmallIntegerField()

    @property
    def result(self):
        return self.requesting_player_score > self.confirming_player_score

    @property
    def winner(self):
        return self.match.requesting_player if self.result else self.match.confirming_player

    @property
    def loser(self):
        return self.match.confirming_player if self.result else self.match.requesting_player

    @property
    def winner_score(self):
        return max(self.requesting_player_score, self.confirming_player_score)

    @property
    def loser_score(self):
        return min(self.requesting_player_score, self.confirming_player_score)
