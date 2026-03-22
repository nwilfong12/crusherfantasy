from django.core.management.base import BaseCommand
from players.models import Player, Vote
from players.glicko import update_player
from datetime import timedelta

GROUP_WINDOW = 5

class Command(BaseCommand):

    help = "Rebuild Glicko ratings"

    def handle(self, *args, **kwargs):

        vote_count = Vote.objects.count()

        if vote_count == 0:
            self.stdout.write("No votes found. Abort.")
            return

        confirm = input("Type YES to rebuild ratings: ")
        if confirm != "YES":
            return

        Player.objects.update(
            glicko_rating=1500,
            glicko_rd=350,
            glicko_vol=0.06,
            value=1500,
            last_rating_update=None
        )

        votes = Vote.objects.select_related("player").order_by("created_at")

        sessions = []
        current = []
        last_time = None

        for vote in votes:

            if not last_time:
                current.append(vote)

            elif vote.created_at - last_time <= timedelta(seconds=GROUP_WINDOW):
                current.append(vote)

            else:
                if len(current) >= 5:
                    sessions.append(current)
                current = [vote]

            last_time = vote.created_at

        if len(current) >= 5:
            sessions.append(current)

        for session in sessions:

            ranked = sorted(session, key=lambda v: v.rank)

            players_ranked = [(v.player, v.rank) for v in ranked]

            for i in range(len(players_ranked)):

                player_i, rank_i = players_ranked[i]
                results = []

                for j in range(len(players_ranked)):

                    if i == j:
                        continue

                    player_j, rank_j = players_ranked[j]

                    if rank_i < rank_j:
                        results.append((player_j, 1))
                    else:
                        results.append((player_j, 0))

                update_player(player_i, results)
                player_i.save()

        self.stdout.write("Glicko rebuild complete")