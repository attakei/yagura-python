"""yagura URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from registration.backends.hmac.views import RegistrationView

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
        path('accounts/', include('registration.backends.hmac.urls')),
    ]

# Django Debug Toolbar(optional)
if settings.DEBUG:
    try:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
    except ImportError:
        pass
