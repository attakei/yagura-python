from django.urls import path
from django.views.generic import TemplateView

from yagura.accounts.views import ProfileEditView, ProfileView, SetTimezoneView

app_name = 'accounts'
urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit', ProfileEditView.as_view(), name='profile-edit'),
    path('profile/timezone', SetTimezoneView.as_view(), name='set-timezone'),
    path(
        'social/login-error',
        TemplateView.as_view(template_name='accounts/social_error.html'),
        name='social-login-error'),
]
