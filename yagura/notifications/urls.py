from django.urls import path

from yagura.notifications.views import ActivateView, AddNotificationView

app_name = 'notifications'
urlpatterns = (
    path(
        'new/sites/<uuid:pk>',
        AddNotificationView.as_view(),
        name='add-extra-recipient'),
    path('activate/<uuid:code>', ActivateView.as_view(), name='activate'),
)
