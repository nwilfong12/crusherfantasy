import math
from django.utils import timezone
from players.models import Vote
from django.db.models import Avg
from players.models import Player
POSITIONS_WEIGHTS={
    1: 1000,
    2: 750,
    3: 500,
    4: 250,
    5: 0
}

HALF_LIFE = 45
MIN_VOTES = 20
GLOBAL_DEFAULT = 500
def time_weight(timestamp):
    age_days = (timezone.now() - timestamp).days
    return math.exp(-age_days / HALF_LIFE)

def vote_score(rank, timestamp):
    weight = time_weight(timestamp)
    return POSITIONS_WEIGHTS[rank] * weight, weight


def calculate_player_value(player):

    votes = Vote.objects.filter(player=player)

    weighted_sum = 0
    total_weight = 0

    for vote in votes:
        score, weight = vote_score(vote.rank, vote.created_at)
        weighted_sum += score
        total_weight += weight

    if total_weight == 0:
        base_score = GLOBAL_DEFAULT
    else:
        base_score = weighted_sum / total_weight

    vote_count = votes.count()

    # global average value across all players
    global_average = Player.objects.aggregate(avg=Avg("value"))["avg"] or GLOBAL_DEFAULT

    # Bayesian smoothing
    smoothed_score = (
        (vote_count / (vote_count + MIN_VOTES)) * base_score
        + (MIN_VOTES / (vote_count + MIN_VOTES)) * global_average
    )

    return smoothed_score