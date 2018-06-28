from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    DetailView, ListView,
)

from yagura.sites.models import Site


class SiteListView(LoginRequiredMixin, ListView):
    model = Site


class SiteDetailView(LoginRequiredMixin, DetailView):
    """Site detail view

    TODO: Custom 404 from request not-found pk
    """
    model = Site
