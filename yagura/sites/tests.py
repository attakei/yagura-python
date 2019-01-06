from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse_lazy
from parameterized import parameterized

from yagura.sites.models import Site
from yagura.sites.templatetags import url_filter
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

    def test_save_basich_auth_url(self):
        site = Site(url='http://user:pass@example.com')
        site.save()

    @parameterized.expand([
        ('http://example.com', None, 'http://example.com'),
        ('http://example.com', 'example', 'example'),
    ])
    def test_display_name(self, url, title, expect):
        site = Site(url=url, title=title)
        assert site.display_name == expect


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

    def test_hidden_disabled_sites(self):
        site: Site = Site.objects.first()
        site.enabled = False
        site.save()
        user = get_user_model().objects.first()
        self.client.force_login(user)
        resp = self.client.get(self.url)
        assert resp.status_code == 200
        assert len(resp.context['site_list']) == 1

    def test_show_all_force(self):
        site: Site = Site.objects.first()
        site.enabled = False
        site.save()
        user = get_user_model().objects.first()
        self.client.force_login(user)
        resp = self.client.get(f'{self.url}?all=1')
        assert resp.status_code == 200
        assert len(resp.context['site_list']) == 2

    def test_show_title_or_url(self):
        self.client.force_login(get_user_model().objects.first())
        resp = self.client.get(self.url)
        # have title
        assert 'examplecom' in str(resp.content)
        # not have title
        assert 'http://example.com/404' in str(resp.content)


class SiteCreate_ViewTest(ViewTestCase):
    url = reverse_lazy('sites:create')
    VALID_FORM_VAL = {
        'url': 'http://example.com/',
        'ok_http_status': 200,
    }

    def test_login_required(self):
        resp = self.client.post(self.url, self.VALID_FORM_VAL)
        assert resp.status_code == 302

    def test_get_form(self):
        user = get_user_model().objects.first()
        self.client.force_login(user)
        resp = self.client.get(self.url)
        assert resp.status_code == 200

    def test_add(self):
        user = get_user_model().objects.create_user('test_user')
        self.client.force_login(user)
        resp = self.client.post(self.url, self.VALID_FORM_VAL)
        assert resp.status_code == 302
        site = Site.objects.filter(url='http://example.com/').first()
        assert site.created_by == user
        assert site.ok_http_status == 200

    def test_add_with_status_code(self):
        user = get_user_model().objects.create_user('test_user')
        self.client.force_login(user)
        resp = self.client.post(
            self.url, {'url': 'http://example.com/', 'ok_http_status': 302})
        assert resp.status_code == 302
        site = Site.objects.filter(url='http://example.com/').first()
        assert site.created_by == user
        assert site.ok_http_status == 302

    @override_settings(YAGURA_SITES_LIMIT=1)
    def test_post_overlimit(self):
        """If settgins has sites-limit, user can register more than limit
        """
        self.test_add()
        resp = self.client.post(self.url, self.VALID_FORM_VAL)
        assert resp.status_code == 200

    @override_settings(YAGURA_SITES_LIMIT=2)
    def test_post_overlimit_safe(self):
        """If settgins has sites-limit, user can register more than limit
        """
        self.test_add()
        resp = self.client.post(self.url, self.VALID_FORM_VAL)
        assert resp.status_code == 302

    @override_settings(YAGURA_SITES_LIMIT=1)
    def test_post_superuser(self):
        """If user is granted as superuser, not limit sites.
        """
        self.client.force_login(get_user_model().objects.first())
        self.client.post(self.url, self.VALID_FORM_VAL)
        values = self.VALID_FORM_VAL.copy()
        values['url'] = 'http://example.com/2'
        resp = self.client.post(self.url, values)
        assert resp.status_code == 302

    @override_settings(YAGURA_SITES_LIMIT=0)
    def test_post_nolimit(self):
        """If settgins has sites-limit, user can register more than limit
        """
        self.test_add()
        resp = self.client.post(self.url, self.VALID_FORM_VAL)
        assert resp.status_code == 302


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
        assert 'examplecom' in str(resp.content)

    def test_not_found(self):
        self.client.force_login(get_user_model().objects.first())
        url = reverse_lazy(
            'sites:detail',
            args=['aaaaaaaa-bbbb-4ccc-dddd-eeeeeeeeee00'])
        resp = self.client.get(url)
        assert resp.status_code == 404


class SiteEditTitle_ViewTest(ViewTestCase):
    url = reverse_lazy(
        'sites:edit-title',
        args=['aaaaaaaa-bbbb-4ccc-dddd-eeeeeeeeee01'])

    def setUp(self):
        super().setUp()
        owner = get_user_model().objects.first()
        Site.objects.update(created_by=owner)

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
            'sites:edit-title',
            args=['aaaaaaaa-bbbb-4ccc-dddd-eeeeeeeeee00'])
        resp = self.client.get(url)
        assert resp.status_code == 404

    def test_post(self):
        self.client.force_login(get_user_model().objects.first())
        resp = self.client.post(self.url, {
            'id': 'aaaaaaaa-bbbb-4ccc-dddd-eeeeeeeeee01',
            'title': 'testsite'
        })
        assert resp.status_code == 302
        assert resp['Location'] == reverse_lazy('sites:list')
        assert Site.objects.first().title == 'testsite'

    def test_only_owner__get(self):
        user = get_user_model().objects.create_user('not-owner')
        self.client.force_login(user)
        resp = self.client.get(self.url)
        assert 'sites/site_edittitle_ng.html' in resp.template_name

    def test_only_owner__post(self):
        user = get_user_model().objects.create_user('not-owner')
        self.client.force_login(user)
        resp = self.client.post(self.url)
        assert resp.status_code == 200

    # def test_after_disabled_new_monitor_log(self):
    #     from yagura.monitors.models import StateHistory
    #     before_ = StateHistory.objects.count()
    #     self.test_confirmed()
    #     after_ = StateHistory.objects.count()
    #     assert before_ + 1 == after_


class SiteDisable_ViewTest(ViewTestCase):
    url = reverse_lazy(
        'sites:disable',
        args=['aaaaaaaa-bbbb-4ccc-dddd-eeeeeeeeee01'])

    def setUp(self):
        super().setUp()
        owner = get_user_model().objects.first()
        Site.objects.update(created_by=owner)

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

    def test_confirmed(self):
        self.client.force_login(get_user_model().objects.first())
        resp = self.client.post(self.url)
        assert resp.status_code == 302
        assert resp['Location'] == reverse_lazy('sites:list')
        assert Site.objects.count() == 2

    def test_only_owner__get(self):
        user = get_user_model().objects.create_user('not-owner')
        self.client.force_login(user)
        resp = self.client.get(self.url)
        assert 'sites/site_disable_ng.html' in resp.template_name

    def test_only_owner__post(self):
        user = get_user_model().objects.create_user('not-owner')
        self.client.force_login(user)
        resp = self.client.post(self.url)
        assert resp.status_code == 200

    def test_after_disabled_new_monitor_log(self):
        from yagura.monitors.models import StateHistory
        before_ = StateHistory.objects.count()
        self.test_confirmed()
        after_ = StateHistory.objects.count()
        assert before_ + 1 == after_


class SiteDelete_ViewTest(ViewTestCase):
    url = reverse_lazy(
        'sites:delete',
        args=['aaaaaaaa-bbbb-4ccc-dddd-eeeeeeeeee01'])

    def setUp(self):
        super().setUp()
        owner = get_user_model().objects.first()
        Site.objects.update(created_by=owner)

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

    def test_confirmed(self):
        self.client.force_login(get_user_model().objects.first())
        resp = self.client.post(self.url)
        assert resp.status_code == 302
        assert resp['Location'] == reverse_lazy('sites:list')
        assert Site.objects.count() == 1

    def test_only_owner__get(self):
        user = get_user_model().objects.create_user('not-owner')
        self.client.force_login(user)
        resp = self.client.get(self.url)
        assert 'sites/site_delete_ng.html' in resp.template_name

    def test_only_owner__post(self):
        user = get_user_model().objects.create_user('not-owner')
        self.client.force_login(user)
        resp = self.client.post(self.url)
        assert resp.status_code == 200

    @override_settings(YAGURA_ENABLE_DELETING_SITES=False)
    def test_guard_by_settings(self):
        self.client.force_login(get_user_model().objects.first())
        resp = self.client.get(self.url)
        assert resp.status_code == 200
        assert 'sites/site_delete_ng.html' in resp.template_name
        assert 'Disabled deleting sites by administrator' in str(resp.content)

    @override_settings(YAGURA_ENABLE_DELETING_SITES=False)
    def test_guard_by_settings_post(self):
        self.client.force_login(get_user_model().objects.first())
        resp = self.client.post(self.url)
        assert resp.status_code == 200
        assert 'sites/site_delete_ng.html' in resp.template_name
        assert 'Disabled deleting sites by administrator' in str(resp.content)
        assert Site.objects.count() == 2


class SafeUrl_Tests(TestCase):
    def test_no_filtered(self):
        before = 'http://example.com'
        after = url_filter.guard_basic_auth(before)
        assert before == after

    def test_basic_filtered(self):
        before = 'http://user:pass@example.com'
        after = url_filter.guard_basic_auth(before)
        assert after == 'http://<basic-auth>@example.com'
