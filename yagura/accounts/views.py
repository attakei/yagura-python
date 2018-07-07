from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from yagura.accounts.forms import ProfileEditForm


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'


class ProfileEditView(LoginRequiredMixin, FormView):
    """Update user profile (name and email only)

    TODO: must be verify changed email is available.
    """
    form_class = ProfileEditForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:profile')

    def get_initial(self):
        user = self.request.user
        fields = self.form_class.Meta.fields
        return {k: getattr(user, k) for k in fields}

    def form_valid(self, form):
        user = self.request.user
        for k in self.form_class.Meta.fields:
            setattr(user, k, form.cleaned_data[k])
        user.save()
        return super().form_valid(form)