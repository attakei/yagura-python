from django.urls import path

from yagura.sites.views import SiteCreateView, SiteDetailView, SiteListView

app_name = 'sites'
urlpatterns = [
    path('', SiteListView.as_view(), name='list'),
    path('new', SiteCreateView.as_view(), name='create'),
    path('<uuid:pk>', SiteDetailView.as_view(), name='detail'),
]
