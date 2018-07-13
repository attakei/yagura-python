from django.contrib.auth import get_user_model
from django.core import mail
from django.urls import reverse_lazy

from yagura.notifications.models import Activation, ExtraRecipient
from yagura.sites.models import Site
from yagura.tests.base import ViewTestCase


class AddNotification_ViewTest(ViewTestCase):
    fixtures = [
        'initial',
        'unittest_suite',
    ]

    url = reverse_lazy(
        'notifications:add-extra-recipient',
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


class Activate_ViewTest(ViewTestCase):
    fixtures = [
        'unittest_suite',
    ]

    def test_activation_enabled(self):
        recipient = ExtraRecipient.objects.create(
            site=Site.objects.first(), email='test@example.com')
        Activation.objects.create(
            recipient=recipient, code='aaaaaaaa-bbbb-4ccc-dddd-eeeeeeeeee01')
        url = reverse_lazy(
            'notifications:activate',
            kwargs={'code': 'aaaaaaaa-bbbb-4ccc-dddd-eeeeeeeeee01'})
        resp = self.client.get(url)
        assert resp.status_code == 200
        recipient = ExtraRecipient.objects.first()
        assert recipient.enabled is True
