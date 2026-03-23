from players.models import Player
import math

def normalize_live():

    players = list(Player.objects.all())
    if not players:
        return

    ratings = [p.glicko_rating for p in players]

    mean = sum(ratings) / len(ratings)
    variance = sum((r - mean) ** 2 for r in ratings) / len(ratings)
    std = math.sqrt(variance)

    if std == 0:
        return

    for p in players:

        z = (p.glicko_rating - mean) / (std * 0.6)

        base = 1 / (1 + math.exp(-1.4 * z))


        curved = base ** 3.8

        p.value = int(curved * 1000)

    Player.objects.bulk_update(players, ["value"])