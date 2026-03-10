from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render
from .models import Player
from django.core.paginator import Paginator
from django.http import JsonResponse

def player_search(request):

    query = request.GET.get("q")

    players = Player.objects.filter(name__icontains=query)[:10]

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

    results = []

    for player in players:

        team_id = TEAM_IDS.get(player.team)

        logo_url = ""
        if team_id:
            logo_url = f"https://cdn.nba.com/logos/nba/{team_id}/global/L/logo.svg"

        results.append({
            "name": player.name,
            "position": player.position,
            "team": player.team,
            "player_id": player.player_id,
            "logo": logo_url
        })

    return JsonResponse({"players": results})
def players_list(request):
    query = request.GET.get("q")
    selected_positions = request.GET.getlist("position")  # ADD THIS

    if not request.session.get("has_voted"):
        return redirect("/")

    players = Player.objects.all()

    if query:
        players = players.filter(name__icontains=query)

    # INSERT POSITION FILTER HERE
    if selected_positions:
        from django.db.models import Q
        position_filter = Q()

        for pos in selected_positions:
            position_filter |= Q(position__icontains=pos)

        players = players.filter(position_filter)

    players = players.order_by("-value")

    # pagination
    paginator = Paginator(players, 50)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    start_rank = (page_obj.number - 1) * paginator.per_page
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
    for player in page_obj:
        team_id = TEAM_IDS.get(player.team)
        if team_id:
            player.logo_url = f"https://cdn.nba.com/logos/nba/{team_id}/global/L/logo.svg"
        else:
            player.logo_url = ""

    return render(request, "players/players_list.html", {
        "page_obj": page_obj,
        "query": query,
        "start_rank": start_rank,
        "selected_positions": selected_positions,
    })