from django.core.management.base import BaseCommand
from players.rating_utils import normalize_live

class Command(BaseCommand):

    help = "Rebuild leaderboard values from Glicko ratings"

    def handle(self, *args, **kwargs):
        normalize_live()
        self.stdout.write(self.style.SUCCESS("Leaderboard now uses Glicko curve"))