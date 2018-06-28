from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse_lazy
from parameterized import parameterized

from yagura.sites.models import Site
from yagura.tests.base import ViewTestCase


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


class SiteList_ViewTest(ViewTestCase):
    url = reverse_lazy('sites:list')

    def test_login_required(self):
        resp = self.client.get(self.url)
        assert resp.status_code == 302

    def test_logined_user(self):
        user = get_user_model().objects.first()
        self.client.force_login(user)
        resp = self.client.get(self.url)
        assert resp.status_code == 200


class SiteCreate_ViewTest(ViewTestCase):
    url = reverse_lazy('sites:create')

    def test_login_required(self):
        resp = self.client.post(self.url, {'url': 'http://example.com/'})
        assert resp.status_code == 302

    def test_get_form(self):
        user = get_user_model().objects.first()
        self.client.force_login(user)
        resp = self.client.get(self.url)
        assert resp.status_code == 200

    def test_add(self):
        user = get_user_model().objects.first()
        self.client.force_login(user)
        resp = self.client.post(self.url, {'url': 'http://example.com/'})
        assert resp.status_code == 302
        site = Site.objects.filter(url='http://example.com/').first()
        assert site.created_by == user


class SiteDetail_ViewTest(ViewTestCase):
    url = reverse_lazy(
        'sites:detail',
        args=['aaaaaaaa-bbbb-4ccc-dddd-eeeeeeeeee01'])

    def test_login_required(self):
        resp = self.client.get(self.url)
        assert resp.status_code == 302

    def test_logined_user(self):
        self.client.force_login(get_user_model().objects.first())
        resp = self.client.get(self.url)
        assert resp.status_code == 200

    def test_not_found(self):
        self.client.force_login(get_user_model().objects.first())
        url = reverse_lazy(
            'sites:detail',
            args=['aaaaaaaa-bbbb-4ccc-dddd-eeeeeeeeee00'])
        resp = self.client.get(url)
        assert resp.status_code == 404
