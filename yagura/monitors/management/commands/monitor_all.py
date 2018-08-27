import asyncio

from django.core.management.base import BaseCommand
from django.utils.timezone import now

from yagura.monitors.services import handle_state, monitor_site
from yagura.sites.models import Site


# TODO: duplicated with \
#   ``yagura.monitors.managements.commands.monitor_site._monitor_site``
async def _monitor_site(site, monitor_date):
    state, reason = await monitor_site(site)
    handle_state(site, state, monitor_date, reason=reason)


class Command(BaseCommand):
    help = 'monitor all websites'

    def handle(self, *args, **options):
        # Main
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(asyncio.gather(*[
            _monitor_site(site, now())
            for site in Site.objects.all()
        ]))
        loop.close()
