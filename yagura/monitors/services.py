import typing
from urllib.error import HTTPError
from urllib.request import urlopen

from django.conf import settings
from templated_email import send_templated_mail

from yagura.monitors.models import StateHistory
from yagura.sites.models import Site
from yagura.utils import get_base_url


def monitor_site(site: Site) -> typing.Tuple[str, str]:
    try:
        resp = urlopen(site.url)
    except HTTPError as err:
        resp = err
    result = 'OK' if resp.code == site.ok_status_code else 'NG'
    reason = f"HTTP status code is {resp.code}" \
        f" (expected: {site.ok_status_code})" \
        if result == 'NG' else ''
    return result, reason


def handle_state(site, state, monitor_date, reason=''):
    current: StateHistory = StateHistory.objects.filter(site=site).last()
    if current is None:
        current: StateHistory = StateHistory.objects.create(
            site=site, state=state, reason=reason)
        send_state_email(current, 'monitors/handle_state_first')
        return
    if current.state == state:
        current.save()
        return
    current.end_at = monitor_date
    current.save()
    current = StateHistory.objects.create(
        site=site, state=state, begin_at=monitor_date, reason=reason)
    send_state_email(current, 'monitors/handle_state_changed')


def send_state_email(current, template_name):
    # For owner
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
    # For extra
    for recipient in current.site.recipients.filter(enabled=True):
        context = {
            'site': current.site,
            'history': current,
            'owner': {'get_full_name': 'Subscriber'},
            'base_url': get_base_url(),
        }
        send_templated_mail(
            template_name=template_name,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient.email],
            context=context,
        )
