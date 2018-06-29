from django import forms
from django.conf import settings

from yagura.sites.models import Site


class SiteCreateForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ['url', ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def clean(self):
        sites_limit = getattr(settings, 'YAGURA_SITES_LIMIT', 1)
        sites_count = Site.objects.filter(created_by=self.request.user).count()
        if sites_count >= sites_limit:
            raise forms.ValidationError(
                'You are reached limits for nums of monitoring sites.')
