from players.models import Player
import math

from players.models import Player

def normalize_live():

    players = list(Player.objects.all().order_by("-glicko_rating"))

    n = len(players)
    if n == 0:
        return

    for i, p in enumerate(players):

        rank_percentile = i / (n - 1)

        value = 1000 - (rank_percentile ** 0.65) * 800

        p.value = int(value)

    Player.objects.bulk_update(players, ["value"])