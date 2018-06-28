from urllib.error import HTTPError
from urllib.request import urlopen
from uuid import UUID

from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import now

from yagura.monitors.models import StateHistory
from yagura.sites.models import Site


def monitor_site(site):
    try:
        resp = urlopen(site.url)
        return 'OK' if resp.code == 200 else 'NG'
    except HTTPError:
        return 'NG'


def handle_state(site, state, monitor_date):
    current = StateHistory.objects.filter(site=site).last()
    if current is None:
        StateHistory.objects.create(site=site, state=state)
        return
    if current.state == state:
        current.save()
        return
    current.end_at = monitor_date
    current.save()
    StateHistory.objects.create(
        site=site, state=state, begin_at=monitor_date)


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
