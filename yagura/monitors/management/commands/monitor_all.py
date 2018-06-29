from django.core.management.base import BaseCommand
from django.utils.timezone import now

from yagura.monitors.services import handle_state, monitor_site
from yagura.sites.models import Site


class Command(BaseCommand):
    help = 'monitor all websites'

    def handle(self, *args, **options):
        # Main
        for site in Site.objects.all():
            monitor_date = now()
            state = monitor_site(site)
            handle_state(site, state, monitor_date)
