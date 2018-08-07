from django.urls import path

from yagura.notifications.views import (
    EmailActivateView, AddNotificationView, AddSlackRecipientView,
    EmailDeactivateCompleteView, EmailDeactivateView, NotificationDeleteCompleteView,
    NotificationDeleteView, EmailRecipientListView, SlackRecipientListView
)

app_name = 'notifications'
urlpatterns = (
    path(
        'sites/<uuid:pk>/new',
        AddNotificationView.as_view(),
        name='add-recipient'),
    # Slack recipient urlconf
    path(
        'sites/<uuid:pk>/slack',
        SlackRecipientListView.as_view(),
        name='list-slack-recipient'),
    path(
        'sites/<uuid:pk>/slack/new',
        AddSlackRecipientView.as_view(),
        name='add-slack-recipient'),
    # Email recipient urlconf
    path(
        'sites/<uuid:pk>/email',
        EmailRecipientListView.as_view(),
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
        EmailActivateView.as_view(),
        name='email-activate'),
    path(
        'emaildeactivate/<uuid:code>',
        EmailDeactivateView.as_view(),
        name='email-deactivate'),
    path(
        'emaildeactivate/complete',
        EmailDeactivateCompleteView.as_view(),
        name='email-deactivate-complete'),
)
