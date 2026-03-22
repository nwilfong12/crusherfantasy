import random
from players.models import Player


def get_matchup():

    players = list(Player.objects.all())

    if len(players) <= 5:
        return players

    players_sorted = sorted(players, key=lambda p: p.glicko_rating, reverse=True)

    top_100 = players_sorted[:100] if len(players_sorted) >= 100 else players_sorted

    def anchor_weight(p):

        strength_rank = players_sorted.index(p) + 1
        strength_weight = max(0, (120 - strength_rank)) / 120

        rd_weight = p.glicko_rd / 350

        return (strength_weight * 3) + (rd_weight * 2) + random.random()

    weights = [anchor_weight(p) for p in players]

    anchor = random.choices(players, weights=weights, k=1)[0]

    WINDOW = 150

    pool = [
        p for p in players
        if abs(p.glicko_rating - anchor.glicko_rating) <= WINDOW
    ]

    if len(pool) < 5:
        pool = players

    matchup = []

    elite_candidates = [p for p in pool if p in top_100]
    random.shuffle(elite_candidates)

    matchup.extend(elite_candidates[:2])

    high_rd_sorted = sorted(pool, key=lambda p: p.glicko_rd, reverse=True)

    for p in high_rd_sorted:
        if p not in matchup:
            matchup.append(p)
            break

    while len(matchup) < 5:
        p = random.choice(pool)
        if p not in matchup:
            matchup.append(p)

    return matchup