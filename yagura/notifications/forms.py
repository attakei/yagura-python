from django import forms
from django.forms import widgets

from yagura.notifications.models import EmailRecipient


class AddNotificationForm(forms.ModelForm):
    class Meta:
        model = EmailRecipient
        fields = ['site', 'email', ]
        widgets = {
            'site': widgets.HiddenInput(),
        }
