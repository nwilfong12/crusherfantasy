from django.db import models

# Create your models here.
class Player(models.Model):
    player_id = models.IntegerField(unique=True, db_index=True)
    name = models.CharField(max_length=100)
    team = models.CharField(max_length=50)
    position = models.CharField(max_length=30)
    age = models.IntegerField(null=True, blank=True)
    value = models.IntegerField(default = 500)
    glicko_rating = models.FloatField(default=1500)
    glicko_rd = models.FloatField(default=350)
    glicko_vol = models.FloatField(default=0.06)
    last_rating_update = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

class VoteSession(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session {self.id}"

class Vote(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    rank = models.IntegerField()
    session = models.ForeignKey(
        VoteSession,
        on_delete=models.CASCADE,
        null=True,      # ⭐ IMPORTANT for migration safety
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
