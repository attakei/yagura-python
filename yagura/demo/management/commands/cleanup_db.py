from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand

from yagura.monitors.models import StateHistory
from yagura.sites.models import Site


class Command(BaseCommand):
    help = 'Clear all application db and init users'

    def handle(self, *args, **options):
        StateHistory.objects.all().delete()
        Site.objects.all().delete()
        self._cleanup_users()

    def _cleanup_users(self):
        get_user_model().objects.all().delete()
        call_command(
            'loaddata', 'initial',
            stdout=self.stdout, stderr=self.stderr)
