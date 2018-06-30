import os
from unittest import mock

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase, override_settings

from yagura.monitors.models import StateHistory
from yagura.sites.models import Site
from yagura.tests.utils import run_command

UserModel = get_user_model()


class CleanupDb_CommandTest(TestCase):
    fixtures = [
        'initial',
        'unittest_suite',
    ]

    def test_init_user(self):
        UserModel.objects.create_user('testuser')
        run_command('cleanup_db')
        assert UserModel.objects.count() == 1

    def test_remove_sites(self):
        run_command('cleanup_db')
        assert Site.objects.count() == 0

    def test_remove_statehistory(self):
        StateHistory.objects.create(
            site=Site.objects.first(), state='OK')
        run_command('cleanup_db')
        assert StateHistory.objects.count() == 0

    @override_settings(YAGURA_DEMO_ADMIN_PASSWORD='Password!?1234')
    def test_change_password_by_settings(self):
        run_command('cleanup_db')
        admin = UserModel.objects.first()
        assert admin.check_password('Password!?1234')

    @mock.patch.dict(
        os.environ, {'YAGURA_DEMO_ADMIN_PASSWORD': 'Password?!1234'})
    def test_change_password_by_env(self):
        run_command('cleanup_db')
        admin = UserModel.objects.first()
        assert admin.check_password('Password?!1234')

    @override_settings(YAGURA_DEMO_ADMIN_EMAIL='dummy@example.com')
    def test_change_email_by_settings(self):
        run_command('cleanup_db')
        admin = UserModel.objects.first()
        assert admin.email == 'dummy@example.com'

    @mock.patch.dict(
        os.environ, {'YAGURA_DEMO_ADMIN_EMAIL': 'admin@example.com'})
    def test_change_email_by_env(self):
        run_command('cleanup_db')
        admin = UserModel.objects.first()
        assert admin.email == 'admin@example.com'

    def test_send_email(self):
        run_command('cleanup_db')
        assert len(mail.outbox) == 1
        mail_body = mail.outbox[0].body
        mail_to = mail.outbox[0].to
        assert 'http://localhost' in mail_body
        assert mail_to == ['root@localhost']
