import typing

import aiohttp
from django.conf import settings
from templated_email import send_templated_mail

from yagura.monitors.models import StateHistory
from yagura.notifications.services import SlackNotifier
from yagura.sites.models import Site
from yagura.utils import get_base_url


# TODO: Test for more cases
async def monitor_site(site: Site) -> typing.Tuple[str, str]:
    async with aiohttp.ClientSession() as client:
        try:
            resp = await client.get(site.url, allow_redirects=False)
            result = 'OK' if resp.status == site.ok_http_status else 'NG'
            reason = f"HTTP status code is {resp.status}" \
                f" (expected: {site.ok_http_status})" \
                if result == 'NG' else ''
        except aiohttp.ClientError as err:
            result = 'NG'
            reason = str(err)
    return result, reason


def handle_state(site, state, monitor_date, reason=''):
    current: StateHistory = StateHistory.objects.filter(site=site).last()
    if current is None:
        current: StateHistory = StateHistory.objects.create(
            site=site, state=state, reason=reason)
        send_state_email(current, 'monitors/handle_state_first')
        for slack_recipient in current.site.slack_recipients.all():
            notifier = SlackNotifier(slack_recipient)
            notifier.send(current, base_url=get_base_url())
        return
    if current.state == state:
        current.save()
        return
    current.end_at = monitor_date
    current.save()
    current = StateHistory.objects.create(
        site=site, state=state, begin_at=monitor_date, reason=reason)
    send_state_email(current, 'monitors/handle_state_changed')
    for slack_recipient in current.site.slack_recipients.all():
        notifier = SlackNotifier(slack_recipient)
        notifier.send(current, base_url=get_base_url())


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
