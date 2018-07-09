from django.urls import path

from yagura.notifications.views import ActivateView

app_name = 'notifications'
urlpatterns = (
    path('activate/<uuid:code>', ActivateView.as_view(), name='activate'),
)
