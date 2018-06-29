import os
from urllib.error import HTTPError
from urllib.request import urlopen

from django.conf import settings
from templated_email import send_templated_mail

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
        current = StateHistory.objects.create(site=site, state=state)
        send_state_email(current, 'monitors/handle_state_first')
        return
    if current.state == state:
        current.save()
        return
    current.end_at = monitor_date
    current.save()
    StateHistory.objects.create(
        site=site, state=state, begin_at=monitor_date)
    send_state_email(current, 'monitors/handle_state_changed')


def send_state_email(current, template_name):
    def _get_base_url():
        key = 'YAGURA_BASE_URL'
        if key in os.environ:
            return os.environ[key]
        elif hasattr(settings, key):
            return getattr(settings, key)
        return 'http://localhost'
    owner = current.site.created_by
    context = {
        'site': current.site,
        'history': current,
        'owner': owner,
        'base_url': _get_base_url(),
    }
    send_templated_mail(
        template_name=template_name,
        from_email='yagura@exemple.com',
        recipient_list=[owner.email],
        context=context,
    )
