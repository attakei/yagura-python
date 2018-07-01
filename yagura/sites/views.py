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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        # TODO: Must save 'created_by' in form cobject
        site = form.instance
        site.created_by = self.request.user
        site.save()
        return super().form_valid(form)