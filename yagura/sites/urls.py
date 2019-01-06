from django.urls import path

from yagura.sites.views import (
    SiteCreateView, SiteDeleteView, SiteDetailView, SiteDisableView,
    SiteListView, SiteEditTitleView
)

app_name = 'sites'
urlpatterns = [
    path('', SiteListView.as_view(), name='list'),
    path('new', SiteCreateView.as_view(), name='create'),
    path('<uuid:pk>', SiteDetailView.as_view(), name='detail'),
    path('<uuid:pk>/edittitle', SiteEditTitleView.as_view(), name='edit-title'),
    path('<uuid:pk>/_disable', SiteDisableView.as_view(), name='disable'),
    path('<uuid:pk>/delete', SiteDeleteView.as_view(), name='delete'),
]
