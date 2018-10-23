"""Test case for yagura.monitors.services
"""
import logging
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


def _call_monitor_site(event_loop, site, mock_url, mock_status):
    with aioresponses() as mocked:
        mocked.get(mock_url, status=mock_status)
        result, reason = event_loop.run_until_complete(monitor_site(site))
    return result, reason


def test_monitor_site__expected_request_200(event_loop, caplog):
    caplog.set_level(logging.DEBUG, logger='yagura.monitors.services')
    url = 'http://example.com/'
    status_code = 200
    site = mock.MagicMock(url=url, ok_http_status=status_code)
    result, reason = _call_monitor_site(event_loop, site, url, status_code)
    assert result == 'OK'
    assert reason == ''
    assert caplog.records[0].msg == 'Start to check: http://example.com/'
    assert len(caplog.records) == 3


def test_monitor_site__expected_request_404(event_loop, caplog):
    caplog.set_level(logging.DEBUG, logger='yagura.monitors.services')
    url = 'http://example.com/'
    status_code = 404
    site = mock.MagicMock(url=url, ok_http_status=status_code)
    result, reason = _call_monitor_site(event_loop, site, url, status_code)
    assert result == 'OK'
    assert reason == ''
    assert caplog.records[0].msg == 'Start to check: http://example.com/'
    assert len(caplog.records) == 3


def test_monitor_site__ng_response_with_reason(event_loop, caplog):
    caplog.set_level(logging.DEBUG, logger='yagura.monitors.services')
    site = mock.MagicMock(url='http://example.com/', ok_http_status=302)
    result, reason = _call_monitor_site(event_loop, site, site.url, 200)
    assert result == 'NG'
    assert reason == 'HTTP status code is 200 (expected: 302)'
    assert caplog.records[0].msg == 'Start to check: http://example.com/'
    assert len(caplog.records) == 3


def test_monitor_site__ng_multiple(event_loop, caplog):
    caplog.set_level(logging.DEBUG, logger='yagura.monitors.services')
    site = mock.MagicMock(url='http://example.com/', ok_http_status=302)
    with aioresponses() as mocked:
        mocked.get(site.url, status=200)
        mocked.get(site.url, status=200)
        mocked.get(site.url, status=200)
        result, reason = event_loop.run_until_complete(monitor_site(site, 3))
        assert result == 'NG'
        assert reason == 'HTTP status code is 200 (expected: 302)'
        assert len(mocked._responses) == 0


def test_monitor_site__ok_once_retry(event_loop, caplog):
    caplog.set_level(logging.DEBUG, logger='yagura.monitors.services')
    site = mock.MagicMock(url='http://example.com/', ok_http_status=200)
    with aioresponses() as mocked:
        mocked.get(site.url, status=503)
        mocked.get(site.url, status=200)
        mocked.get(site.url, status=200)
        result, reason = event_loop.run_until_complete(monitor_site(site, 3))
        assert result == 'OK'
        assert len(mocked._responses) == 1


def test_monitor_site__urlerror(event_loop):
    site = mock.MagicMock(url='http://example.com/', ok_http_status=302)
    with aioresponses() as mocked:
        mocked.get(site.url, exception=ClientError('Test error'))
        result, reason = event_loop.run_until_complete(monitor_site(site))
        assert result == 'NG'
        assert reason == 'Test error'


class SendStateEmail_Test(TestCase):
    fixtures = [
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
