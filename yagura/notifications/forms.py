from django import forms
from django.forms import widgets

from yagura.notifications.models import EmailRecipient, SlackRecipient


class AddNotificationForm(forms.ModelForm):
    class Meta:
        model = EmailRecipient
        fields = ['site', 'email', ]
        widgets = {
            'site': widgets.HiddenInput(),
        }


class AddSlackRecipientForm(forms.ModelForm):
    class Meta:
        model = SlackRecipient
        fields = ['site', 'url', 'channel', ]
        widgets = {
            'site': widgets.HiddenInput(),
        }
