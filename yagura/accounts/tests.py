from django.contrib.auth import get_user_model

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
