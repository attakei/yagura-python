from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse_lazy
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


class SiteList_ViewTest(TestCase):
    fixtures = [
        'unittest_suite',
    ]

    url = reverse_lazy('sites:list')

    def test_login_required(self):
        client = Client()
        resp = client.get(self.url)
        assert resp.status_code == 302

    def test_logined_user(self):
        get_user_model().objects.create_user('test')
        client = Client()
        client.force_login(get_user_model().objects.first())
        resp = client.get(self.url)
        assert resp.status_code == 200


class SiteCreate_ViewTest(TestCase):
    fixtures = [
        'initial',
        'unittest_suite',
    ]

    url = reverse_lazy('sites:create')

    def test_login_required(self):
        client = Client()
        resp = client.post(self.url, {'url': 'http://example.com/'})
        assert resp.status_code == 302

    def test_add(self):
        user = get_user_model().objects.first()
        client = Client()
        client.force_login(user)
        resp = client.post(self.url, {'url': 'http://example.com/'})
        assert resp.status_code == 302
        site = Site.objects.first()
        assert site.created_by == user


class SiteDetail_ViewTest(TestCase):
    fixtures = [
        'initial',
        'unittest_suite',
    ]

    url = reverse_lazy(
        'sites:detail',
        args=['aaaaaaaa-bbbb-4ccc-dddd-eeeeeeeeee01'])

    def test_login_required(self):
        client = Client()
        resp = client.get(self.url)
        assert resp.status_code == 302

    def test_logined_user(self):
        client = Client()
        client.force_login(get_user_model().objects.first())
        resp = client.get(self.url)
        assert resp.status_code == 200

    def test_not_found(self):
        client = Client()
        client.force_login(get_user_model().objects.first())
        url = reverse_lazy(
            'sites:detail',
            args=['aaaaaaaa-bbbb-4ccc-dddd-eeeeeeeeee00'])
        resp = client.get(url)
        assert resp.status_code == 404
