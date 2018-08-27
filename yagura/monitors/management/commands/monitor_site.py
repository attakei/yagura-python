import asyncio
from uuid import UUID

from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import now

from yagura.monitors.services import handle_state, monitor_site
from yagura.sites.models import Site


# TODO: duplicated with \
#   ``yagura.monitors.managements.commands.monitor_all._monitor_site``
async def _monitor_site(site, monitor_date):
    state, reason = await monitor_site(site)
    handle_state(site, state, monitor_date, reason=reason)


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
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(_monitor_site(site, monitor_date))
        loop.close()
