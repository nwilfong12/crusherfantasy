from django.shortcuts import render, redirect
import random

from players.models import Player, Vote
from players.glicko import update_player
from players.rating_utils import normalize_live
from players.matchmaking import get_matchup


def vote_page(request):

    if request.method == "POST":

        if "skip_vote" in request.POST:
            return redirect("/vote/")

        selections = {}

        for key in request.POST:
            if key.startswith("player_"):
                player_id = int(key.split("_")[1])
                rank = int(request.POST.get(key))
                selections[player_id] = rank

        ranks = list(selections.values())
        if sorted(ranks) != [1, 2, 3, 4, 5]:
            return redirect("/vote/")

        session_players = []

        for player_id, rank in selections.items():
            player = Player.objects.get(id=player_id)

            Vote.objects.create(
                player=player,
                rank=rank
            )

            session_players.append((player, rank))

        session_players.sort(key=lambda x: x[1])

        for i in range(len(session_players)):

            player_i, rank_i = session_players[i]
            results = []

            for j in range(len(session_players)):
                if i == j:
                    continue

                player_j, rank_j = session_players[j]

                if rank_i < rank_j:
                    results.append((player_j, 1))
                else:
                    results.append((player_j, 0))

            update_player(player_i, results)
            player_i.save()

        normalize_live()

        first_vote = not request.session.get("has_voted", False)
        request.session["has_voted"] = True

        if first_vote:
            return redirect("/players/")
        else:
            return redirect("/vote/")

    players = list(Player.objects.all())

    if len(players) >= 5:
        selected_players = get_matchup()
    else:
        selected_players = players

    TEAM_IDS = {
        "Hawks": "1610612737",
        "Celtics": "1610612738",
        "Nets": "1610612751",
        "Hornets": "1610612766",
        "Bulls": "1610612741",
        "Cavaliers": "1610612739",
        "Mavericks": "1610612742",
        "Nuggets": "1610612743",
        "Pistons": "1610612765",
        "Warriors": "1610612744",
        "Rockets": "1610612745",
        "Pacers": "1610612754",
        "Clippers": "1610612746",
        "Lakers": "1610612747",
        "Grizzlies": "1610612763",
        "Heat": "1610612748",
        "Bucks": "1610612749",
        "Timberwolves": "1610612750",
        "Pelicans": "1610612740",
        "Knicks": "1610612752",
        "Thunder": "1610612760",
        "Magic": "1610612753",
        "76ers": "1610612755",
        "Suns": "1610612756",
        "Trail Blazers": "1610612757",
        "Kings": "1610612758",
        "Spurs": "1610612759",
        "Raptors": "1610612761",
        "Jazz": "1610612762",
        "Wizards": "1610612764",
    }

    for player in selected_players:
        team_id = TEAM_IDS.get(player.team)
        if team_id:
            player.logo_url = f"https://cdn.nba.com/logos/nba/{team_id}/global/L/logo.svg"
        else:
            player.logo_url = ""

    return render(request, "voting/voting.html", {
        "players": selected_players
    })