from django.urls import path

from yagura.notifications.views import (
    ActivateView, AddNotificationView, AddSlackRecipientView,
    DeactivateCompleteView, DeactivateView, NotificationDeleteCompleteView,
    NotificationDeleteView, NotificationListView
)

app_name = 'notifications'
urlpatterns = (
    path(
        'sites/<uuid:pk>/new',
        AddNotificationView.as_view(),
        name='add-recipient'),
    path(
        'sites/<uuid:pk>/slack/new',
        AddSlackRecipientView.as_view(),
        name='add-slack-recipient'),
    # Email recipient urlconf
    path(
        'sites/<uuid:pk>/email',
        NotificationListView.as_view(),
        name='list-email-recipient'),
    path(
        'email/<int:pk>/delete',
        NotificationDeleteView.as_view(),
        name='delete-email-recipient'),
    path(
        'delete/complete',
        NotificationDeleteCompleteView.as_view(),
        name='delete-email-complete'),
    path(
        'emailactivate/<uuid:code>',
        ActivateView.as_view(),
        name='email-activate'),
    path(
        'emaildeactivate/<uuid:code>',
        DeactivateView.as_view(),
        name='email-deactivate'),
    path(
        'emaildeactivate/complete',
        DeactivateCompleteView.as_view(),
        name='email-deactivate-complete'),
)
