import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand
from templated_email import send_templated_mail

from yagura.utils import get_base_url


class Command(BaseCommand):
    help = 'Clear all application db and init users'

    def handle(self, *args, **options):
        self._run_command('flush', '--noinput')
        self._run_command('loaddata', 'initial')
        if hasattr(settings, 'YAGURA_DEMO_ADMIN_PASSWORD'):
            user = get_user_model().objects.get(username='admin')
            user.set_password(settings.YAGURA_DEMO_ADMIN_PASSWORD)
            user.save()
        if 'YAGURA_DEMO_ADMIN_PASSWORD' in os.environ:
            user = get_user_model().objects.get(username='admin')
            user.set_password(os.environ['YAGURA_DEMO_ADMIN_PASSWORD'])
            user.save()
        send_templated_mail(
            template_name='demo/cleanup_db',
            from_email='yagura@exemple.com',
            recipient_list=['admin@example.com', ],
            context={
                'base_url': get_base_url(),
            },
        )

    def _run_command(self, *args):
        """Shortcut of call_command that bind stdout and stderr
        """
        call_command(*args, stdout=self.stdout, stderr=self.stderr)
