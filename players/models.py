from django.db import models

# Create your models here.
class Player(models.Model):
    player_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    team = models.CharField(max_length=50)
    position = models.CharField(max_length=10)
    value = models.IntegerField(default = 500)

    def __str__(self):
        return self.name

class Vote(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    rank = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)