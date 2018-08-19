from unittest import mock

from django.test import TestCase

from yagura.notifications.models import SlackRecipient
from yagura.notifications.services import SlackNotifier
from yagura.sites.models import Site


class SlackNotification_ModelTest(TestCase):
    fixtures = [
        'unittest_suite',
    ]

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
