from django.contrib.auth import get_user_model
from django.core import mail
from django.urls import reverse_lazy

from yagura.notifications.models import Activation, Deactivation, Recipient
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
        Recipient.objects.create(
            site=Site.objects.get(pk='aaaaaaaa-bbbb-4ccc-dddd-eeeeeeeeee01'),
            email='test@example.com', enabled=True)

    def test_post_not_delete(self):
        resp = self.client.post(
            reverse_lazy('notifications:delete-recipient', args=(1,)))
        assert resp.status_code == 302
        assert Recipient.objects.count() == 1
        assert Deactivation.objects.count() == 1
        assert len(mail.outbox) == 1


class Activate_ViewTest(ViewTestCase):
    fixtures = [
        'unittest_suite',
    ]

    def test_activation_enabled(self):
        recipient = Recipient.objects.create(
            site=Site.objects.first(), email='test@example.com')
        Activation.objects.create(
            recipient=recipient, code='aaaaaaaa-bbbb-4ccc-dddd-eeeeeeeeee01')
        url = reverse_lazy(
            'notifications:activate',
            kwargs={'code': 'aaaaaaaa-bbbb-4ccc-dddd-eeeeeeeeee01'})
        resp = self.client.get(url)
        assert resp.status_code == 200
        recipient = Recipient.objects.first()
        assert recipient.enabled is True


class Deactivate_ViewTest(ViewTestCase):
    fixtures = [
        'unittest_suite',
    ]

    def test_invalid_code(self):
        url = reverse_lazy(
            'notifications:deactivate',
            kwargs={'code': 'aaaaaaaa-bbbb-4ccc-dddd-eeeeeeeeee01'})
        resp = self.client.get(url)
        assert resp.status_code == 404

    def test_deactivation_enabled(self):
        recipient = Recipient.objects.create(
            site=Site.objects.first(), email='test@example.com', enabled=True)
        Deactivation.objects.create(
            recipient=recipient, code='aaaaaaaa-bbbb-4ccc-dddd-eeeeeeeeee01')
        url = reverse_lazy(
            'notifications:deactivate',
            kwargs={'code': 'aaaaaaaa-bbbb-4ccc-dddd-eeeeeeeeee01'})
        resp = self.client.get(url)
        assert resp.status_code == 302
        assert Recipient.objects.count() == 0
        resp = self.client.get(resp['Location'])
        assert resp.status_code == 200
