"""Test case for yagura.monitors.services
"""
import os
from unittest import mock

from aiohttp import ClientError
from aioresponses import aioresponses
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase, override_settings
from parameterized import parameterized

from yagura.monitors.models import StateHistory
from yagura.monitors.services import monitor_site, send_state_email
from yagura.sites.models import Site


class MonitorSite_Test(TestCase):
    @parameterized.expand([
        ('http://example.com/200', 200, 'OK'),
        ('http://example.com/404', 404, 'OK'),
    ])
    async def test_expected_request(
            self, url, status_code, exp_result):
        with aioresponses() as mocked:
            mocked.get(url, status=status_code)
            site = mock.MagicMock(url=url, ok_http_status=status_code)
            result, reason = await monitor_site(site)
            assert result == exp_result
            assert reason == ''

    @aioresponses()
    async def test_ng_response_with_reason(self, mocked):
        site = mock.MagicMock(url='http://example.com/', ok_http_status=302)
        mocked.get(site.url, statusq=200)
        result, reason = await monitor_site(site)
        assert result == 'NG'
        assert reason == \
            'HTTP status code is 200 (expected: 302)'

    @aioresponses()
    async def test_urlerror(self, mocked):
        site = mock.MagicMock(
            url='http://example.com/200', ok_http_status=302)
        mocked.get(site.url, exception=ClientError('Test error'))
        result, reason = await monitor_site(site)
        assert result == 'NG'
        assert reason == 'Test error'


class SendStateEmail_Test(TestCase):
    fixtures = [
        'initial',
        'unittest_suite',
    ]

    def setUp(self):
        super().setUp()
        owner = get_user_model().objects.first()
        Site.objects.update(created_by=owner)

    @parameterized.expand([
        ('monitors/handle_state_changed', ),
        ('monitors/handle_state_first', ),
    ])
    def test_default(self, template_name):
        current = StateHistory.objects.create(
            site=Site.objects.first(), state='OK')
        send_state_email(current, template_name)
        assert len(mail.outbox) == 1
        mail_body = mail.outbox[0].body
        assert 'http://localhost' in mail_body

    @parameterized.expand([
        ('monitors/handle_state_changed', ),
        ('monitors/handle_state_first', ),
    ])
    @mock.patch.dict(os.environ, {'YAGURA_BASE_URL': 'http://localhost:8000'})
    def test_use_environ(self, template_name):
        current = StateHistory.objects.create(
            site=Site.objects.first(), state='OK')
        send_state_email(current, template_name)
        assert len(mail.outbox) == 1
        mail_body = mail.outbox[0].body
        assert 'http://localhost:8000' in mail_body

    @parameterized.expand([
        ('monitors/handle_state_changed', ),
        ('monitors/handle_state_first', ),
    ])
    @override_settings(YAGURA_BASE_URL='https://example.jp')
    def test_use_settings(self, template_name):
        current = StateHistory.objects.create(
            site=Site.objects.first(), state='OK')
        send_state_email(current, template_name)
        assert len(mail.outbox) == 1
        mail_body = mail.outbox[0].body
        assert 'https://example.jp' in mail_body

    @override_settings(DEFAULT_FROM_EMAIL='test@example.com')
    def test_from_email(self):
        current = StateHistory.objects.create(
            site=Site.objects.first(), state='OK')
        send_state_email(current, 'monitors/handle_state_first')
        mail_from = mail.outbox[0].from_email
        assert mail_from == 'test@example.com'

    @parameterized.expand([
        ('monitors/handle_state_changed', ),
        ('monitors/handle_state_first', ),
    ])
    def test_use_user_full_name(self, template_name):
        user = get_user_model().objects.first()
        user.first_name = 'test'
        user.last_name = 'admin'
        user.save()
        current = StateHistory.objects.create(
            site=Site.objects.first(), state='OK')
        send_state_email(current, template_name)
        mail_body = mail.outbox[0].body
        assert 'test admin' in mail_body

    @parameterized.expand([
        (True, 2),
        (False, 1),
    ])
    def test_send_recipients(self, recipient_enabled, expect_mails):
        from yagura.notifications.models import EmailRecipient
        EmailRecipient.objects.create(
            site=Site.objects.first(),
            email='test2@example.com', enabled=recipient_enabled)
        current = StateHistory.objects.create(
            site=Site.objects.first(), state='OK')
        send_state_email(current, 'monitors/handle_state_first')
        assert len(mail.outbox) == expect_mails
