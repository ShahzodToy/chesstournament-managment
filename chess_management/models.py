from django.db import models
from users.models import *

class Tournament(models.Model):
    name = models.CharField(max_length=100, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    participants = models.ManyToManyField(User, related_name='tournaments')
    current_round = models.IntegerField(default=1)
    def __str__(self):
        return f"{self.name} and {self.id}"

    
class Match(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='matches')
    round_number = models.IntegerField()
    player1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player1_matches',null=True, blank=True)
    player2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player2_matches',null=True, blank=True)
    result = models.CharField(max_length=20, choices=[('player1', 'Player 1 Wins'), ('player2', 'Player 2 Wins'), ('draw', 'Draw')], null=True, blank=True)

    def __str__(self):
        return f"Round {self.round_number} - {self.player1} vs {self.player2} and {self.id}"
    


