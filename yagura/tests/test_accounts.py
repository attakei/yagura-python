"""Regular test case for django-registration and django-auth apps
"""
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import Client, TestCase, override_settings
from django.urls import reverse_lazy

User = get_user_model()


class Login_ViewTest(TestCase):
    fixtures = ['initial', ]
    test_url = reverse_lazy('login')

    def test_get(self):
        client = Client()
        resp = client.get(self.test_url)
        assert resp.status_code == 200

    def test_post(self):
        client = Client()
        resp = client.post(
            self.test_url, {'username': 'admin', 'password': 'Yagura!!'})
        assert resp.status_code == 302


class Registration_ViewTest(TestCase):
    test_url = reverse_lazy('registration_register')

    def _test_valid_post(self):
        client = Client()
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'Pa?SSw0rd!',
            'password2': 'Pa?SSw0rd!',
        }
        resp = client.post(self.test_url, form_data)
        assert resp.status_code == 302
        assert len(mail.outbox) == 1

    def test_default_mail(self):
        self._test_valid_post()
        mail_body = mail.outbox[0].body
        activate_url = reverse_lazy(
            'registration_activate', args=['ACTIVATE', ])
        activate_url = activate_url.replace('ACTIVATE/', '')
        assert str(activate_url) in mail_body
        from_email = mail.outbox[0].from_email
        assert from_email == 'noreply@example.com'

    @override_settings(DEFAULT_FROM_EMAIL='admin@example.com')
    def test_custom_mail(self):
        self._test_valid_post()
        mail_body = mail.outbox[0].body
        activate_url = reverse_lazy(
            'registration_activate', args=['ACTIVATE', ])
        activate_url = activate_url.replace('ACTIVATE/', '')
        assert str(activate_url) in mail_body
        from_email = mail.outbox[0].from_email
        assert from_email == 'admin@example.com'
