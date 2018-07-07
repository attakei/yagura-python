from django import forms
from django.contrib.auth import get_user_model


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fields['email'].required = True
