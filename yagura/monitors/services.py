from urllib.error import HTTPError
from urllib.request import urlopen

from yagura.monitors.models import StateHistory


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
