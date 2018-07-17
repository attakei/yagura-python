from django import forms
from django.forms import widgets

from yagura.notifications.models import Recipient


class AddNotificationForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ['site', 'email', ]
        widgets = {
            'site': widgets.HiddenInput(),
        }
