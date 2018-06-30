from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Clear all application db and init users'

    def handle(self, *args, **options):
        self._run_command('flush', '--noinput')
        self._run_command('loaddata', 'initial')

    def _run_command(self, *args):
        """Shortcut of call_command that bind stdout and stderr
        """
        call_command(*args, stdout=self.stdout, stderr=self.stderr)
