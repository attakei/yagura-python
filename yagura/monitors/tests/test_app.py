import pytest
import requests_mock
from django.contrib.auth import get_user_model
from django.core import mail
from django.core.management.base import CommandError
from django.test import TestCase

from yagura.monitors.models import StateHistory
from yagura.sites.models import Site
from yagura.tests.utils import run_command


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

    def test_site_found(self):
        test_uuid = 'aaaaaaaa-bbbb-4ccc-dddd-eeeeeeeeee01'
        site = Site.objects.get(pk=test_uuid)
        with requests_mock.mock() as m:
            m.get(site.url, status_code=200)
            run_command('monitor_site', test_uuid)
        assert StateHistory.objects.count() == 1
        state = StateHistory.objects.first()
        assert state.state == 'OK'

    def test_site_redirect(self):
        test_uuid = 'aaaaaaaa-bbbb-4ccc-dddd-eeeeeeeeee01'
        site = Site.objects.get(pk=test_uuid)
        site.url = 'https://httpstat.us/302'
        site.save()
        run_command('monitor_site', test_uuid)
        assert StateHistory.objects.count() == 1
        state = StateHistory.objects.first()
        assert state.state == 'NG'

    def test_site_not_found(self):
        test_uuid = 'aaaaaaaa-bbbb-4ccc-dddd-eeeeeeeeee02'
        site = Site.objects.get(pk=test_uuid)
        with requests_mock.mock() as m:
            m.get(site.url, status_code=404)
            run_command('monitor_site', test_uuid)
        assert StateHistory.objects.count() == 1
        state = StateHistory.objects.first()
        assert state.state == 'NG'
        assert len(mail.outbox) == 1
        assert '(expected: 200)' in state.reason

    def test_site_expected_not_found(self):
        test_uuid = 'aaaaaaaa-bbbb-4ccc-dddd-eeeeeeeeee02'
        site = Site.objects.get(pk=test_uuid)
        site.ok_http_status = 404
        site.save()
        with requests_mock.mock() as m:
            m.get(site.url, status_code=404)
            run_command('monitor_site', test_uuid)
        assert StateHistory.objects.count() == 1
        state = StateHistory.objects.first()
        assert state.state == 'OK'
        assert len(mail.outbox) == 1

    def test_keep_state(self):
        test_uuid = 'aaaaaaaa-bbbb-4ccc-dddd-eeeeeeeeee01'
        site = Site.objects.get(pk=test_uuid)
        self.test_site_found()
        before_updated = StateHistory.objects.first().updated_at
        with requests_mock.mock() as m:
            m.get(site.url, status_code=200)
            run_command('monitor_site', test_uuid)
        assert StateHistory.objects.count() == 1
        after_updated = StateHistory.objects.first().updated_at
        assert before_updated != after_updated

    def test_change_state(self):
        test_uuid = 'aaaaaaaa-bbbb-4ccc-dddd-eeeeeeeeee01'
        self.test_site_found()
        site = Site.objects.get(pk=test_uuid)
        with requests_mock.mock() as m:
            m.get(site.url, status_code=404)
            run_command('monitor_site', test_uuid)
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

    def test_save_all_states(self):
        with requests_mock.mock() as m:
            for site in Site.objects.all():
                m.get(site.url, status_code=site.ok_http_status)
            run_command('monitor_all')
        assert StateHistory.objects.count() == 2

    def test_states_not_changed(self):
        self.test_save_all_states()
        with requests_mock.mock() as m:
            for site in Site.objects.all():
                m.get(site.url, status_code=site.ok_http_status)
            run_command('monitor_all')
        assert StateHistory.objects.count() == 2

    def test_states_changed(self):
        self.test_save_all_states()
        with requests_mock.mock() as m:
            for site in Site.objects.all():
                m.get(site.url, status_code=200)
            site = Site.objects.first()
            m.get(site.url, status_code=404)
            run_command('monitor_all')
        assert StateHistory.objects.count() == 3
