from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from yagura.tests.base import ViewTestCase


class Profile_ViewTest(ViewTestCase):
    fixtures = [
        'initial',
    ]
    url = '/accounts/profile/'

    def test_login_required(self):
        resp = self.client.get(self.url)
        assert resp.status_code == 302

    def test_logged_in(self):
        self.client.force_login(get_user_model().objects.first())
        resp = self.client.get(self.url)
        assert resp.status_code == 200


class ProfileEdit_ViewTest(ViewTestCase):
    fixtures = [
        'initial',
    ]
    url = reverse_lazy('accounts:profile-edit')

    def test_login_required(self):
        resp = self.client.get(self.url)
        assert resp.status_code == 302

    def test_logged_in_get(self):
        self.client.force_login(get_user_model().objects.first())
        resp = self.client.get(self.url)
        assert resp.status_code == 200

    def test_update_first_name(self):
        user = get_user_model().objects.first()
        self.client.force_login(user)
        before_ = user.first_name
        resp = self.client.post(
            self.url, {'first_name': 'test', 'email': 'test@example.com'})
        assert resp.status_code == 302
        after_ = get_user_model().objects.first().first_name
        assert before_ != after_

    def test_email_require(self):
        user = get_user_model().objects.first()
        self.client.force_login(user)
        resp = self.client.post(self.url, {'first_name': 'test'})
        assert resp.status_code == 200
