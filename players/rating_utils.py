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

        z = (p.glicko_rating - mean) / std

        base = 1 / (1 + math.exp(-1.8 * z))

        curved = base ** 1.6

        value = 150 + curved * 850

        p.value = int(value)

    Player.objects.bulk_update(players, ["value"])