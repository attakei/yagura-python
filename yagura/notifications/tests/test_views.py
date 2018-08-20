from django.contrib.auth import get_user_model
from django.core import mail
from django.urls import reverse_lazy
from parameterized import parameterized

from yagura.notifications.models import (
    EmailActivation, EmailDeactivation, EmailRecipient, SlackRecipient
)
from yagura.sites.models import Site
from yagura.tests.base import ViewTestCase


class EmailRecipientCreate_ViewTest(ViewTestCase):
    fixtures = [
        'unittest_suite',
    ]

    url = reverse_lazy(
        'notifications:add-recipient',
        args=['aaaaaaaa-bbbb-4ccc-dddd-eeeeeeeeee01'])

    def test_login_required(self):
        resp = self.client.get(self.url)
        assert resp.status_code == 302

    @parameterized.expand([
        (2, ),
        (3, ),
    ])
    def test_logged_in(self, user_id):
        self.client.force_login(get_user_model().objects.get(pk=user_id))
        resp = self.client.get(self.url)
        assert resp.status_code == 200

    @parameterized.expand([
        (2, ),
        (3, ),
    ])
    def test_post_anyone(self, user_id):
        user = get_user_model().objects.get(pk=user_id)
        self.client.force_login(user)
        resp = self.client.post(self.url, {
            'site': 'aaaaaaaa-bbbb-4ccc-dddd-eeeeeeeeee01',
            'email': 'dummy@example.com'})
        assert resp.status_code == 302
        assert len(mail.outbox) == 1
        assert EmailRecipient.objects.count() == 1
        recipient = EmailRecipient.objects.first()
        assert recipient.created_by == user


class EmailRecipientDelete_ViewTest(ViewTestCase):
    fixtures = [
        'initial',
        'unittest_suite',
    ]

    def setUp(self):
        super().setUp()
        self.client.force_login(get_user_model().objects.first())
        site = Site.objects.get(pk='aaaaaaaa-bbbb-4ccc-dddd-eeeeeeeeee01')
        EmailRecipient.objects.create(
            site=site, email='test2@example.com',
            enabled=True, created_by_id=2)
        EmailRecipient.objects.create(
            site=site, email='test3@example.com',
            enabled=True, created_by_id=3)

    @parameterized.expand([
        (1, 2, True, 'Site owner can delete all recipient'),
        (2, 2, True, 'Site owner can delete all recipient'),
        (1, 3, False, 'Other user cannot delete recipient'),
        (2, 3, True, 'Recipient owner can delete it'),
    ])
    def test_get(self, r_id, u_id, can_delete, desc):
        user = get_user_model().objects.get(pk=u_id)
        self.client.force_login(user)
        resp = self.client.get(
            reverse_lazy('notifications:delete-email-recipient', args=(r_id,)))
        assert resp.status_code == 200
        if can_delete:
            assert 'You do not have permission' not in str(resp.content)
        else:
            assert 'You do not have permission' in str(resp.content)

    @parameterized.expand([
        (1, 2, True, 'Site owner can delete all recipient'),
        (2, 2, True, 'Site owner can delete all recipient'),
        (1, 3, False, 'Other user cannot delete recipient'),
        (2, 3, True, 'Recipient owner can delete it'),
    ])
    def test_post(self, r_id, u_id, can_delete, desc):
        user = get_user_model().objects.get(pk=u_id)
        self.client.force_login(user)
        resp = self.client.post(
            reverse_lazy('notifications:delete-email-recipient', args=(r_id,)))
        if can_delete:
            assert resp.status_code == 302
            assert EmailRecipient.objects.count() == 2
            assert EmailDeactivation.objects.count() == 1
            assert len(mail.outbox) == 1
        else:
            assert resp.status_code == 200
            assert EmailRecipient.objects.count() == 2
            assert EmailDeactivation.objects.count() == 0
            assert len(mail.outbox) == 0


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


class SlackRecipientCreate_ViewTest(ViewTestCase):
    fixtures = [
        'unittest_suite',
    ]

    url = reverse_lazy(
        'notifications:add-slack-recipient',
        args=['aaaaaaaa-bbbb-4ccc-dddd-eeeeeeeeee01'])

    def test_login_required(self):
        resp = self.client.get(self.url)
        assert resp.status_code == 302

    @parameterized.expand([
        (2, ),
        (3, ),
    ])
    def test_logged_in(self, user_id):
        self.client.force_login(get_user_model().objects.get(pk=user_id))
        resp = self.client.get(self.url)
        assert resp.status_code == 200

    @parameterized.expand([
        (2, ),
        (3, ),
    ])
    def test_post_anyone(self, user_id, ):
        user = get_user_model().objects.get(pk=user_id)
        self.client.force_login(user)
        resp = self.client.post(self.url, {
            'site': 'aaaaaaaa-bbbb-4ccc-dddd-eeeeeeeeee01',
            'url': 'http://example.com'})
        assert resp.status_code == 302
        assert SlackRecipient.objects.count() == 1
        recipient = SlackRecipient.objects.first()
        assert recipient.created_by == user


class SlackRecipientDelete_ViewTest(ViewTestCase):
    fixtures = [
        'initial',
        'unittest_suite',
    ]

    def setUp(self):
        super().setUp()
        self.site = Site.objects.first()
        SlackRecipient.objects.create(
            site=self.site, url='http://example.com', created_by_id=2)
        SlackRecipient.objects.create(
            site=self.site, url='http://example.com', created_by_id=3)

    @parameterized.expand([
        (1, 2, True, 'Site owner can delete all recipient'),
        (2, 2, True, 'Site owner can delete all recipient'),
        (1, 3, False, 'Other user cannot delete recipient'),
        (2, 3, True, 'Recipient owner can delete it'),
    ])
    def test_get(self, r_id, u_id, can_delete, desc):
        user = get_user_model().objects.get(pk=u_id)
        self.client.force_login(user)
        resp = self.client.get(
            reverse_lazy('notifications:delete-slack-recipient', args=(r_id,)))
        assert resp.status_code == 200
        assert self.site.url in str(resp.content)
        if can_delete:
            assert 'You do not have permission' not in str(resp.content)
        else:
            assert 'You do not have permission' in str(resp.content)

    @parameterized.expand([
        (1, 2, True, 'Site owner can delete all recipient'),
        (2, 2, True, 'Site owner can delete all recipient'),
        (1, 3, False, 'Other user cannot delete recipient'),
        (2, 3, True, 'Recipient owner can delete it'),
    ])
    def test_post(self, r_id, u_id, can_delete, desc):
        user = get_user_model().objects.get(pk=u_id)
        self.client.force_login(user)
        resp = self.client.post(
            reverse_lazy('notifications:delete-slack-recipient', args=(r_id,)))
        if can_delete:
            assert resp.status_code == 302
            assert SlackRecipient.objects.count() == 1
            location = resp['Location']
            assert location == self.site.get_absolute_url()
        else:
            assert resp.status_code == 200
            assert SlackRecipient.objects.count() == 2
