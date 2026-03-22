from django.core.management.base import BaseCommand
from players.models import Vote, VoteSession
from datetime import timedelta


class Command(BaseCommand):

    help = "Group old votes into sessions"

    def handle(self, *args, **kwargs):

        votes = Vote.objects.order_by("created_at")

        current_session = None
        last_time = None

        for vote in votes:

            if not last_time or vote.created_at - last_time > timedelta(seconds=8):
                current_session = VoteSession.objects.create()

            vote.session = current_session
            vote.save()

            last_time = vote.created_at

        self.stdout.write("Vote sessions built")