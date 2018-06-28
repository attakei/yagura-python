from urllib.error import HTTPError
from urllib.request import urlopen

from django.core.management.base import BaseCommand
from django.utils.timezone import now

from yagura.monitors.models import StateHistory
from yagura.sites.models import Site


class Command(BaseCommand):
    help = 'monitor all websites'

    def handle(self, *args, **options):
        # Main
        for site in Site.objects.all():
            print(site)
            monitor_date = now()
            try:
                resp = urlopen(site.url)
                state = 'OK' if resp.code == 200 else 'NG'
            except HTTPError:
                state = 'NG'
            current = StateHistory.objects.filter(site=site).last()
            if current is None:
                StateHistory.objects.create(site=site, state=state)
                continue
            if current.state == state:
                current.save()
                continue
            current.end_at = monitor_date
            current.save()
            StateHistory.objects.create(
                site=site, state=state, begin_at=monitor_date)
