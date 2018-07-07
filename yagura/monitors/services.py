from urllib.error import HTTPError
from urllib.request import urlopen

from django.conf import settings
from templated_email import send_templated_mail

from yagura.monitors.models import StateHistory
from yagura.utils import get_base_url


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
    current = StateHistory.objects.create(
        site=site, state=state, begin_at=monitor_date)
    send_state_email(current, 'monitors/handle_state_changed')


def send_state_email(current, template_name):
    owner = current.site.created_by
    context = {
        'site': current.site,
        'history': current,
        'owner': owner,
        'base_url': get_base_url(),
    }
    send_templated_mail(
        template_name=template_name,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[owner.email],
        context=context,
    )
