from django.core.management.base import BaseCommand
from players.models import Player, VoteSession
from players.glicko import update_player


class Command(BaseCommand):

    help = "Rebuild Glicko ratings using REAL vote sessions"

    def handle(self, *args, **kwargs):

        session_count = VoteSession.objects.count()

        if session_count == 0:
            self.stdout.write("No vote sessions found. Abort.")
            return

        confirm = input("Type YES to rebuild ratings: ")
        if confirm != "YES":
            return

        # HARD RESET RATINGS
        Player.objects.update(
            glicko_rating=1500,
            glicko_rd=350,
            glicko_vol=0.06,
            value=1500,
            last_rating_update=None
        )

        sessions = (
            VoteSession.objects
            .prefetch_related("vote_set__player")
            .order_by("created_at")
        )

        processed = 0

        for session in sessions:

            votes = list(session.vote_set.all())

            # skip broken sessions
            if len(votes) < 5:
                continue

            ranked = sorted(votes, key=lambda v: v.rank)

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

            processed += 1

            if processed % 500 == 0:
                self.stdout.write(f"Processed {processed} sessions...")

        self.stdout.write(self.style.SUCCESS("Glicko rebuild complete"))