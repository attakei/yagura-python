from django.urls import path

from yagura.accounts.views import ProfileView

app_name = 'accounts'
urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
]
