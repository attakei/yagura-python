"""Test case for yagura.monitors.services
"""
import os
from unittest import mock

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase, override_settings
from parameterized import parameterized

from yagura.monitors.models import StateHistory
from yagura.monitors.services import send_state_email
from yagura.sites.models import Site


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
