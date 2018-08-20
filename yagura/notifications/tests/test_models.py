from unittest import mock

from django.contrib.auth import get_user_model
from django.test import TestCase
from parameterized import parameterized

from yagura.notifications.models import EmailRecipient, SlackRecipient
from yagura.notifications.services import SlackNotifier
from yagura.sites.models import Site


class EmailRecipient_ModelTest(TestCase):
    fixtures = [
        'unittest_suite',
    ]

    @parameterized.expand([
        (2, 2, True),
        (3, 2, True),
        (2, 3, False),
    ])
    def test_can_delete(self, created_by, access_by, expected):
        site = Site.objects.first()
        recipient = EmailRecipient(
            site=site, created_by_id=created_by, email='dummy@example.com')
        user = get_user_model().objects.get(pk=access_by)
        assert recipient.can_delete(user) is expected


class SlackNotification_ModelTest(TestCase):
    fixtures = [
        'unittest_suite',
    ]

    @parameterized.expand([
        (2, 2, True),
        (3, 2, True),
        (2, 3, False),
    ])
    def test_can_delete(self, created_by, access_by, expected):
        site = Site.objects.first()
        recipient = SlackRecipient(
            site=site, created_by_id=created_by, url='http://example.com')
        user = get_user_model().objects.get(pk=access_by)
        assert recipient.can_delete(user) is expected

    def test_notification(self):
        site = Site.objects.first()
        recipient = SlackRecipient.objects.create(
            site=site, url='http://example.com')
        current_state = mock.MagicMock(
            site=site, state='NG', reason='Testing error')
        notifier = SlackNotifier(recipient)
        notifier.slack = mock.MagicMock()
        notifier.send(current_state)
        assert notifier.slack.notify.called
        _, called_kwargs = notifier.slack.notify.call_args
        message = called_kwargs['text']
        assert site.url in message
        assert current_state.state in message

    def test_notification_with_channel(self):
        site = Site.objects.first()
        recipient = SlackRecipient.objects.create(
            site=site, url='http://example.com', channel='dummy')
        current_state = mock.MagicMock(
            site=site, state='NG', reason='Testing error')
        notifier = SlackNotifier(recipient)
        notifier.slack = mock.MagicMock()
        notifier.send(current_state)
        assert notifier.slack.notify.called
        _, called_kwargs = notifier.slack.notify.call_args
        assert 'channel' in called_kwargs
