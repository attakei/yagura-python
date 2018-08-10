from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView
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


# TODO: Set message
class SiteCreateView(LoginRequiredMixin, CreateView):
    model = Site
    form_class = SiteCreateForm
    initial = {
        'ok_http_status': 200,
    }

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


# TODO: Set message
class SiteDeleteView(LoginRequiredMixin, DeleteView):
    model = Site
    success_url = reverse_lazy('sites:list')

    def get_template_names(self):
        if self.object.created_by == self.request.user:
            return ['sites/site_confirm_delete.html']
        return ['sites/site_delete_ng.html']

    def post(self, request, *args, **kwargs):
        site = self.get_object()
        if site.created_by == request.user:
            return super().post(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)
