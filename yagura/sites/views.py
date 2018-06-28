from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from yagura.sites.models import Site


class SiteListView(LoginRequiredMixin, ListView):
    model = Site
