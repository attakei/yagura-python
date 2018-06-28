from django import forms

from yagura.sites.models import Site


class SiteCreateForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ['url', ]
