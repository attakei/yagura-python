import asyncio
import importlib
import logging
import random
import time
import typing

import aiohttp
import requests
from django.conf import settings
from django.utils.timezone import now
from requests.exceptions import RequestException
from templated_email import send_templated_mail

from yagura.monitors.models import StateHistory
from yagura.notifications.services import SlackNotifier
from yagura.sites.models import Site
from yagura.utils import get_base_url

Logger = logging.getLogger(__name__)


async def monitor_site_requests(site: Site, max_retry: int = 1) \
        -> typing.Tuple[str, str]:
    """Monitor target site.

    if status unmatch for excepted, retry max argument request
    """
    Logger.debug(f"Start to check: {site.url}")
    for try_idx in range(max_retry):
        try:
            resp = requests.get(site.url, allow_redirects=False)
            Logger.debug(f"Status {resp.status_code}: {site.url}")
            result = 'OK' if resp.status_code == site.ok_http_status else 'NG'
            reason = f"HTTP status code is {resp.status_code}" \
                f" (expected: {site.ok_http_status})" \
                if result == 'NG' else ''
        except RequestException as err:
            result = 'NG'
            reason = f"{err.__class__.__name__} occurred:"
            if str(err) != 'None':
                reason += f" {err}"
        if result == 'OK':
            break
    Logger.debug(f"Finish to check: {site.url}")
    return result, reason


# TODO: Test for more cases
async def monitor_site_aiohttp(site: Site, max_retry: int = 1) \
        -> typing.Tuple[str, str]:
    """Monitor target site.

    if status unmatch for excepted, retry max argument request
    """
    Logger.debug(f"Start to check: {site.url}")
    if not site.enabled:
        return 'DISABLED', ''
    async with aiohttp.ClientSession() as client:
        for try_idx in range(max_retry):
            # FIXME:
            if try_idx != 0:
                time.sleep(random.random() + 1)
            try:
                resp = await client.get(site.url, allow_redirects=False)
                Logger.debug(f"Status {resp.status}: {site.url}")
                result = 'OK' if resp.status == site.ok_http_status else 'NG'
                reason = f"HTTP status code is {resp.status}" \
                    f" (expected: {site.ok_http_status})" \
                    if result == 'NG' else ''
            except aiohttp.ClientError as err:
                result = 'NG'
                reason = f"{err.__class__.__name__} occurred:"
                if str(err) != 'None':
                    reason += f" {err}"
            if result == 'OK':
                break
    Logger.debug(f"Finish to check: {site.url}")
    return result, reason


# TODO: Consider coding testcase
def post_disabled_monitoring(site: Site):
    """Post proc in disable request
    """
    if site.enabled:
        Logger.debug('Passed enabled site')
        return
    handle_state(site, 'DISABLED', now(), 'Disabled manually')


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


class MonitoringJob(object):
    """Monitoring and handler actions managemant job
    """
    def __init__(self):
        self._tasks = []
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)

    def add_task_form_site(self, site):
        """Set monitoring target site
        """
        self._tasks.append(self.monitor_task(site, now()))

    def wait_complete(self):
        """Wait to complete added all tasks
        """
        future = asyncio.gather(*self._tasks)
        self._loop.run_until_complete(future)
        self._loop.close()

    async def monitor_task(self, site, monitor_date):
        """Coroutine to monitor with handlers
        """
        max_retry = settings.YAGURA_MAX_TRY_IN_MONITOR
        func_name = settings.YAGURA_MONITOR_FUNC.split('.')
        package_ = importlib.import_module('.'.join(func_name[:-1]))
        func_ = getattr(package_, func_name[-1])
        state, reason = await func_(site, max_retry)
        if state != 'DISABLED':
            handle_state(site, state, monitor_date, reason=reason)
