from django.contrib.auth import get_user_model
from django.test import Client, TestCase


class FixtureTest(TestCase):
    fixtures = ['initial', ]

    def test_password(self):
        User = get_user_model()
        user = User.objects.first()
        assert user.check_password('Yagura!!')


class IndexTest(TestCase):
    def test_has_title_tag(self):
        client = Client()
        resp = client.get('/')
        assert '<title>Yagura' in str(resp.content)
