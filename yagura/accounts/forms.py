from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import get_language


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fields['email'].required = True


# TODO: Not test
class SetLanguageForm(forms.Form):
    next = forms.URLField(widget=forms.HiddenInput)
    language = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control-lg'}),
        choices=settings.LANGUAGES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['language'].initial = get_language()
