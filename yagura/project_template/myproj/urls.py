from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from registration.backends.default.views import RegistrationView

from yagura.accounts.forms import AccountRegistrationForm

urlpatterns = [
    path('', include('yagura.core.urls')),
    path('sites/', include('yagura.sites.urls')),
    path('notifications/', include('yagura.notifications.urls')),
    path('accounts/', include('yagura.accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('social_django.urls', namespace='social')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
]

if settings.YAGURA_ENABLE_PASSWORD_REGISTRATION:
    urlpatterns += [
        path(
            'accounts/register/',
            RegistrationView.as_view(form_class=AccountRegistrationForm),
            name='registration_register'),
        path('accounts/', include('registration.backends.default.urls')),
    ]
