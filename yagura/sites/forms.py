from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from yagura.sites.models import Site


class SiteCreateForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ['url', 'ok_http_status', ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def clean(self):
        # TODO: Implements method only to check site limit
        if self.request.user.is_superuser:
            return
        sites_limit = getattr(settings, 'YAGURA_SITES_LIMIT', 1)
        # 'limit is 0' mean 'no limit'
        if sites_limit == 0:
            return
        sites_count = Site.objects.filter(created_by=self.request.user).count()
        if sites_count >= sites_limit:
            raise forms.ValidationError(
                _('You are reached limits for nums of monitoring sites.'))
