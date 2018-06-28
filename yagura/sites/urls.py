from django.urls import path

from yagura.sites.views import SiteListView

app_name = 'sites'
urlpatterns = [
    path('', SiteListView.as_view(), name='list'),
]
