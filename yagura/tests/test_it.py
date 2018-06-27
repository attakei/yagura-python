from django.contrib.auth import get_user_model
from django.test import TestCase


class FixtureTest(TestCase):
    fixtures = ['initial', ]

    def test_password(self):
        User = get_user_model()
        user = User.objects.first()
        assert user.check_password('Yagura!!')
