from django import forms
from django.forms import widgets

from yagura.notifications.models import ExtraRecipient


class AddNotificationForm(forms.ModelForm):
    class Meta:
        model = ExtraRecipient
        fields = ['site', 'email', ]
        widgets = {
            'site': widgets.HiddenInput(),
        }
