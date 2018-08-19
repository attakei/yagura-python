from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.core import mail
from django.urls import reverse_lazy

from yagura.notifications.models import (
    EmailActivation, EmailDeactivation, EmailRecipient, SlackRecipient
)
from yagura.sites.models import Site
from yagura.tests.base import ViewTestCase


class AddNotification_ViewTest(ViewTestCase):
    fixtures = [
        'initial',
        'unittest_suite',
    ]

    url = reverse_lazy(
        'notifications:add-recipient',
        args=['aaaaaaaa-bbbb-4ccc-dddd-eeeeeeeeee01'])

    def test_login_required(self):
        resp = self.client.get(self.url)
        assert resp.status_code == 302

    def test_logged_in(self):
        self.client.force_login(get_user_model().objects.first())
        resp = self.client.get(self.url)
        assert resp.status_code == 200

    def test_post(self):
        self.client.force_login(get_user_model().objects.first())
        resp = self.client.post(self.url, {
            'site': 'aaaaaaaa-bbbb-4ccc-dddd-eeeeeeeeee01',
            'email': 'dummy@example.com'})
        assert resp.status_code == 302
        assert len(mail.outbox) == 1


class NotificationDelete_ViewTest(ViewTestCase):
    fixtures = [
        'initial',
        'unittest_suite',
    ]

    def setUp(self):
        super().setUp()
        self.client.force_login(get_user_model().objects.first())
        EmailRecipient.objects.create(
            site=Site.objects.get(pk='aaaaaaaa-bbbb-4ccc-dddd-eeeeeeeeee01'),
            email='test@example.com', enabled=True)

    def test_post_not_delete(self):
        resp = self.client.post(
            reverse_lazy('notifications:delete-email-recipient', args=(1,)))
        assert resp.status_code == 302
        assert EmailRecipient.objects.count() == 1
        assert EmailDeactivation.objects.count() == 1
        assert len(mail.outbox) == 1


class Activate_ViewTest(ViewTestCase):
    fixtures = [
        'unittest_suite',
    ]

    def test_activation_enabled(self):
        recipient = EmailRecipient.objects.create(
            site=Site.objects.first(), email='test@example.com')
        EmailActivation.objects.create(
            recipient=recipient, code='aaaaaaaa-bbbb-4ccc-dddd-eeeeeeeeee01')
        url = reverse_lazy(
            'notifications:email-activate',
            kwargs={'code': 'aaaaaaaa-bbbb-4ccc-dddd-eeeeeeeeee01'})
        resp = self.client.get(url)
        assert resp.status_code == 200
        recipient = EmailRecipient.objects.first()
        assert recipient.enabled is True


class Deactivate_ViewTest(ViewTestCase):
    fixtures = [
        'unittest_suite',
    ]

    def test_invalid_code(self):
        url = reverse_lazy(
            'notifications:email-deactivate',
            kwargs={'code': 'aaaaaaaa-bbbb-4ccc-dddd-eeeeeeeeee01'})
        resp = self.client.get(url)
        assert resp.status_code == 404

    def test_deactivation_enabled(self):
        recipient = EmailRecipient.objects.create(
            site=Site.objects.first(), email='test@example.com', enabled=True)
        EmailDeactivation.objects.create(
            recipient=recipient, code='aaaaaaaa-bbbb-4ccc-dddd-eeeeeeeeee01')
        url = reverse_lazy(
            'notifications:email-deactivate',
            kwargs={'code': 'aaaaaaaa-bbbb-4ccc-dddd-eeeeeeeeee01'})
        resp = self.client.get(url)
        assert resp.status_code == 302
        assert EmailRecipient.objects.count() == 0
        resp = self.client.get(resp['Location'])
        assert resp.status_code == 200


class SlackRecipientDelete_ViewTest(ViewTestCase):
    fixtures = [
        'initial',
        'unittest_suite',
    ]

    def setUp(self):
        super().setUp()
        self.client.force_login(get_user_model().objects.first())
        self.site = Site.objects.first()
        SlackRecipient.objects.create(
            site=self.site, url='http://example.com')

    def test_get(self):
        resp = self.client.get(
            reverse_lazy('notifications:delete-slack-recipient', args=(1,)))
        assert resp.status_code == 200
        assert self.site.url in str(resp.content)

    def test_post(self):
        resp = self.client.post(
            reverse_lazy('notifications:delete-slack-recipient', args=(1,)))
        assert resp.status_code == 302
        assert SlackRecipient.objects.count() == 0
        assert len(get_messages(resp.wsgi_request)) == 1
        location = resp['Location']
        assert location == self.site.get_absolute_url()
        resp = self.client.get(location)
        assert resp.status_code == 200
