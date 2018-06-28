from django.urls import path

from yagura.sites.views import (
	SiteDetailView, SiteListView,
)

app_name = 'sites'
urlpatterns = [
    path('', SiteListView.as_view(), name='list'),
    path('<uuid:pk>', SiteDetailView.as_view(), name='detail'),
]
