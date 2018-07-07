from django.urls import path

from yagura.accounts.views import ProfileEditView, ProfileView

app_name = 'accounts'
urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit', ProfileEditView.as_view(), name='profile-edit'),
]
