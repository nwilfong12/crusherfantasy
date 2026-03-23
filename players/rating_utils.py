from players.models import Player
import math

def normalize_live():

    players = list(Player.objects.all().order_by("-glicko_rating"))

    n = len(players)
    if n == 0:
        return

    for i, p in enumerate(players):

        rank_pct = i / (n - 1)


        value = 1000 - (rank_pct ** 0.72) * 750

        p.value = int(value)

    Player.objects.bulk_update(players, ["value"])