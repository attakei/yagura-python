from django.urls import reverse_lazy

from yagura.notifications.models import Activation, ExtraRecipient
from yagura.sites.models import Site
from yagura.tests.base import ViewTestCase


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
