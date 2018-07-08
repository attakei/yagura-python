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
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),
    path('sites/', include('yagura.sites.urls')),
    path('accounts/', include('yagura.accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('registration.backends.hmac.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
]
