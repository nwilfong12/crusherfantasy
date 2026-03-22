import math
from django.utils import timezone

SCALE = 173.7178

def g(phi):
    return 1 / math.sqrt(1 + 3 * phi**2 / math.pi**2)

def E(mu, mu_j, phi_j):
    return 1 / (1 + math.exp(-g(phi_j) * (mu - mu_j)))

def update_player(player, results):

    mu = (player.glicko_rating - 1500) / SCALE
    phi = player.glicko_rd / SCALE

    v_inv = 0
    delta_sum = 0

    for opponent, score in results:

        mu_j = (opponent.glicko_rating - 1500) / SCALE
        phi_j = opponent.glicko_rd / SCALE

        g_val = g(phi_j)
        E_val = E(mu, mu_j, phi_j)

        v_inv += g_val**2 * E_val * (1 - E_val)
        delta_sum += g_val * (score - E_val)

    if v_inv == 0:
        return

    v = 1 / v_inv

    mu_new = mu + (phi**2) * delta_sum
    phi_new = math.sqrt(1 / (1/phi**2 + 1/v))

    player.glicko_rating = 1500 + SCALE * mu_new
    player.glicko_rd = SCALE * phi_new
    player.last_rating_update = timezone.now()


    player.value = player.glicko_rating