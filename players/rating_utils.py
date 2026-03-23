from players.models import Player
import math

def normalize_live():

    players = list(Player.objects.all())

    if not players:
        return

    sorted_players = sorted(players, key=lambda p: p.glicko_rating, reverse=True)
    active_pool = sorted_players[:150]

    ratings = [p.glicko_rating for p in active_pool]

    mean = sum(ratings) / len(ratings)
    variance = sum((r - mean) ** 2 for r in ratings) / len(ratings)
    std = math.sqrt(variance)

    for p in players:

        z = (p.glicko_rating - mean) / std

        base = 1 / (1 + math.exp(-1.8 * z))
        curved = base ** 3.2

        p.value = int(curved * 1000)

    Player.objects.bulk_update(players, ["value"])