from django.test import TestCase, override_settings
from parameterized import parameterized

from yagura.sites.models import Site


class Site_ModelTest(TestCase):
    @parameterized.expand([
        (
            '443af180-4086-402d-8222-1f6aa5522993',
            '/sites/443af180-4086-402d-8222-1f6aa5522993'),
        (
            '90585392-7e20-4b36-8020-01da52078427',
            '/sites/90585392-7e20-4b36-8020-01da52078427'),
    ])
    @override_settings(ROOT_URLCONF='yagura.sites.tests')
    def test_url(self, site_id, site_url):
        site = Site(id=site_id)
        assert site.get_absolute_url() == site_url
