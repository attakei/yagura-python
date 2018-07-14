from django.urls import path

from yagura.notifications.views import (
    ActivateView, AddNotificationView, NotificationListView
)

app_name = 'notifications'
urlpatterns = (
    path(
        'new/sites/<uuid:pk>',
        AddNotificationView.as_view(),
        name='add-extra-recipient'),
    path(
        'sites/<uuid:pk>',
        NotificationListView.as_view(),
        name='list-extra-recipient'),
    path('activate/<uuid:code>', ActivateView.as_view(), name='activate'),
)
