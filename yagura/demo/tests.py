from django.contrib.auth import get_user_model
from django.test import TestCase

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
