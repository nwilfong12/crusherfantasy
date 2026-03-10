from django.core.management.base import BaseCommand
from players.models import Player
from nba_api.stats.static import players
from nba_api.stats.endpoints import commonplayerinfo
import time


class Command(BaseCommand):
    help = "Import active NBA players with team and position"

    def handle(self, *args, **kwargs):

        nba_players = players.get_active_players()

        for p in nba_players:
            try:
                info = commonplayerinfo.CommonPlayerInfo(player_id=p["id"])
                data = info.get_normalized_dict()["CommonPlayerInfo"][0]

                name = data["DISPLAY_FIRST_LAST"]
                team = data["TEAM_NAME"]
                position = data["POSITION"]
                player_id = p["id"]

                Player.objects.update_or_create(
                    name=name,
                    defaults={
                        "player_id": player_id,
                        "team": team,
                        "position": position,
                        "value": 500
                    }
                )

                print(f"Imported {name}")

                time.sleep(0.6)  # prevents API rate limits

            except Exception as e:
                print("Error importing:", p["full_name"], e)

        self.stdout.write(self.style.SUCCESS("Players imported successfully"))