from django.test import TestCase

from yagura.sites.models import Site


class SiteState_ModelTest(TestCase):
    fixtures = [
        'unittest_suite',
    ]

    def test_relationship(self):
        site = Site.objects.first()
        assert site.states.count() == 0
