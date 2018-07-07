from unittest import mock
from urllib.error import HTTPError

import pytest
from django.contrib.auth import get_user_model
from django.core import mail
from django.core.management.base import CommandError
from django.test import TestCase
from django.utils.six import StringIO

from yagura.monitors.models import StateHistory
from yagura.sites.models import Site
from yagura.tests.utils import run_command


def mocked_urlopen(*args, **kwargs):
    class MockResponse(object):
        def __init__(self, status_code):
            self.code = status_code

    url = args[0]
    if url[-3:] == '200':
        return MockResponse(200)
    raise HTTPError(url=url, code=404, msg='Failure', hdrs='', fp=StringIO())


class StateHistory_ModelTest(TestCase):
    fixtures = [
        'unittest_suite',
    ]

    def test_relationship(self):
        site = Site.objects.first()
        assert site.states.count() == 0


class MonitorSite_CommandTest(TestCase):
    fixtures = [
        'initial',
        'unittest_suite',
    ]

    def setUp(self):
        super().setUp()
        owner = get_user_model().objects.first()
        Site.objects.update(created_by=owner)

    def test_not_uuid(self):
        with pytest.raises(CommandError) as err:
            run_command('monitor_site', '1')
        assert 'must be UUID' in str(err)

    def test_site_not_in_db(self):
        test_uuid = 'aaaaaaaa-bbbb-4ccc-dddd-eeeeeeeeee00'
        with pytest.raises(CommandError) as err:
            run_command('monitor_site', test_uuid)
        assert 'not found' in str(err)

    @mock.patch(
        'yagura.monitors.services.urlopen',
        side_effect=mocked_urlopen
    )
    def test_site_found(self, mock_get):
        test_uuid = 'aaaaaaaa-bbbb-4ccc-dddd-eeeeeeeeee01'
        out, err = run_command('monitor_site', test_uuid)
        assert StateHistory.objects.count() == 1
        state = StateHistory.objects.first()
        assert state.state == 'OK'

    @mock.patch(
        'yagura.monitors.services.urlopen',
        side_effect=mocked_urlopen
    )
    def test_site_not_found(self, mock_get):
        test_uuid = 'aaaaaaaa-bbbb-4ccc-dddd-eeeeeeeeee02'
        out, err = run_command('monitor_site', test_uuid)
        assert StateHistory.objects.count() == 1
        state = StateHistory.objects.first()
        assert state.state == 'NG'
        assert len(mail.outbox) == 1

    @mock.patch(
        'yagura.monitors.services.urlopen',
        side_effect=mocked_urlopen
    )
    def test_keep_state(self, mock_get):
        self.test_site_found()
        before_updated = StateHistory.objects.first().updated_at
        test_uuid = 'aaaaaaaa-bbbb-4ccc-dddd-eeeeeeeeee01'
        out, err = run_command('monitor_site', test_uuid)
        assert StateHistory.objects.count() == 1
        after_updated = StateHistory.objects.first().updated_at
        assert before_updated != after_updated

    @mock.patch(
        'yagura.monitors.services.urlopen',
        side_effect=mocked_urlopen
    )
    def test_change_state(self, mock_get):
        test_uuid = 'aaaaaaaa-bbbb-4ccc-dddd-eeeeeeeeee01'
        self.test_site_found()
        site = Site.objects.first()
        site.url += '/404'
        site.save()
        out, err = run_command('monitor_site', test_uuid)
        assert StateHistory.objects.count() == 2
        before = StateHistory.objects.first()
        after = StateHistory.objects.last()
        assert before.end_at == after.begin_at
        assert len(mail.outbox) == 2
        mail_body = mail.outbox[1].body
        assert 'changing state' in mail_body
        assert 'NG' in mail_body


class MonitorAll_CommandTest(TestCase):
    fixtures = [
        'initial',
        'unittest_suite',
    ]

    def setUp(self):
        super().setUp()
        owner = get_user_model().objects.first()
        Site.objects.update(created_by=owner)

    @mock.patch(
        'yagura.monitors.services.urlopen',
        side_effect=mocked_urlopen
    )
    def test_save_all_states(self, mock_get):
        out, err = run_command('monitor_all')
        print(StateHistory.objects.first().site)
        assert StateHistory.objects.count() == 2

    @mock.patch(
        'yagura.monitors.services.urlopen',
        side_effect=mocked_urlopen
    )
    def test_states_not_changed(self, mock_get):
        self.test_save_all_states()
        out, err = run_command('monitor_all')
        assert StateHistory.objects.count() == 2

    @mock.patch(
        'yagura.monitors.services.urlopen',
        side_effect=mocked_urlopen
    )
    def test_states_changed(self, mock_get):
        self.test_save_all_states()
        site = Site.objects.first()
        site.url += '403'
        site.save()
        out, err = run_command('monitor_all')
        assert StateHistory.objects.count() == 3
