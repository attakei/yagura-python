from django.urls import path

from yagura.notifications.views import (
    EmailActivateView, EmailDeactivateCompleteView, EmailDeactivateView,
    EmailRecipientCreateView, EmailRecipientDeleteCompleteView,
    EmailRecipientDeleteView, EmailRecipientListView, SlackRecipientCreateView,
    SlackRecipientDeleteView, SlackRecipientListView
)

app_name = 'notifications'
urlpatterns = (
    path(
        'sites/<uuid:pk>/new',
        EmailRecipientCreateView.as_view(),
        name='add-recipient'),
    # Slack recipient urlconf
    path(
        'sites/<uuid:pk>/slack',
        SlackRecipientListView.as_view(),
        name='list-slack-recipient'),
    path(
        'sites/<uuid:pk>/slack/new',
        SlackRecipientCreateView.as_view(),
        name='add-slack-recipient'),
    path(
        'slack/<int:pk>/delete',
        SlackRecipientDeleteView.as_view(),
        name='delete-slack-recipient'),
    # Email recipient urlconf
    path(
        'sites/<uuid:pk>/email',
        EmailRecipientListView.as_view(),
        name='list-email-recipient'),
    path(
        'email/<int:pk>/delete',
        EmailRecipientDeleteView.as_view(),
        name='delete-email-recipient'),
    path(
        'delete/complete',
        EmailRecipientDeleteCompleteView.as_view(),
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
