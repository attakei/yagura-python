from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from yagura.sites.forms import SiteCreateForm
from yagura.sites.models import Site


class SiteListView(LoginRequiredMixin, ListView):
    model = Site


class SiteDetailView(LoginRequiredMixin, DetailView):
    """Site detail view

    TODO: Custom 404 from request not-found pk
    """
    model = Site


class SiteCreateView(LoginRequiredMixin, CreateView):
    model = Site
    form_class = SiteCreateForm

    def form_valid(self, form):
        site = form.instance
        site.created_by = self.request.user
        site.save()
        return super().form_valid(form)
