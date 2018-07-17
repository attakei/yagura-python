from django.urls import path

from yagura.notifications.views import (
    ActivateView, AddNotificationView, DeactivateView,
    NotificationDeleteCompleteView, NotificationDeleteView,
    NotificationListView
)

app_name = 'notifications'
urlpatterns = (
    path(
        'sites/<uuid:pk>/new',
        AddNotificationView.as_view(),
        name='add-recipient'),
    path(
        'sites/<uuid:pk>',
        NotificationListView.as_view(),
        name='list-recipient'),
    path(
        '<int:pk>/delete',
        NotificationDeleteView.as_view(),
        name='delete-recipient'),
    path(
        'delete/complete',
        NotificationDeleteCompleteView.as_view(),
        name='delete-complete'),
    path('activate/<uuid:code>', ActivateView.as_view(), name='activate'),
    path(
        'deactivate/<uuid:code>',
        DeactivateView.as_view(),
        name='deactivate'),
)
