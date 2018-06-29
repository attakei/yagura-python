from uuid import UUID

from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import now

from yagura.monitors.services import handle_state, monitor_site
from yagura.sites.models import Site


class Command(BaseCommand):
    help = 'monitor specified website'

    def add_arguments(self, parser):
        parser.add_argument('site_id', type=str)

    def handle(self, *args, **options):
        site_id = options['site_id']
        # Validation
        try:
            UUID(site_id)
        except ValueError:
            raise CommandError(f"Argument must be UUID")
        # Main
        monitor_date = now()
        try:
            site = Site.objects.get(pk=site_id)
        except Site.DoesNotExist:
            raise CommandError(f"Site is not found")
        state = monitor_site(site)
        handle_state(site, state, monitor_date)
