from players.models import Player

def normalize_live():

    players = list(Player.objects.all().order_by("-glicko_rating"))

    n = len(players)
    if n == 0:
        return

    for i, p in enumerate(players):

        percentile = 1 - (i / (n - 1))   # 1 → best player

        value = 1000 * (percentile ** 0.55)

        p.value = int(value)

    Player.objects.bulk_update(players, ["value"])