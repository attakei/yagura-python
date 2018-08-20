from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView, TemplateView
from django.views.generic.edit import FormMixin
from templated_email import send_templated_mail

from yagura.notifications.forms import (
    EmailRecipientCreateForm, SlackRecipientCreateForm,
    SlackRecipientDeleteForm
)
from yagura.notifications.models import (
    EmailActivation, EmailDeactivation, EmailRecipient, SlackRecipient
)
from yagura.sites.models import Site
from yagura.utils import get_base_url


# TODO: Set message
class EmailRecipientCreateView(LoginRequiredMixin, FormMixin, DetailView):
    model = Site
    form_class = EmailRecipientCreateForm
    template_name = 'notifications/emailrecipient_form.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['site'] = self.object
        return initial

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            recipient = form.instance
            recipient.created_by = request.user
            recipient.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        activation = EmailActivation.generate_code(form.instance)
        send_templated_mail(
            template_name='notifications/emailrecipient_confirm_activate',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[form.instance.email],
            context={
                'site': form.instance.site,
                'recipient': form.instance,
                'activation': activation,
                'base_url': get_base_url(),
            }
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'sites:detail', args=(self.object.id, ))


# TODO: Set message
class EmailRecipientDeleteView(LoginRequiredMixin, DetailView):
    model = EmailRecipient
    template_name = 'notifications/emailrecipient_confirm_delete.html'

    def post(self, request, *args, **kwargs):
        recipient = self.get_object()
        if not recipient.can_delete(request.user):
            # TODO: Add error message
            return self.get(request, *args, **kwargs)
        deactivation = EmailDeactivation.generate_code(recipient)
        send_templated_mail(
            template_name='notifications/emailrecipient_confirm_delete',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient.email],
            context={
                'site': recipient.site,
                'recipient': recipient,
                'deactivation': deactivation,
                'base_url': get_base_url(),
            }
        )
        # TODO: Redirect to site-detail
        return HttpResponseRedirect(
            reverse_lazy('notifications:delete-email-complete'))


# TODO: Not need, when redirect to site-detail
class EmailRecipientDeleteCompleteView(LoginRequiredMixin, TemplateView):
    template_name = 'notifications/emailrecipient_complete_delete.html'


class EmailRecipientListView(LoginRequiredMixin, ListView):
    model = EmailRecipient

    def get_queryset(self):
        qs_ = super().get_queryset()
        return qs_.filter(site_id=self.kwargs['pk'])

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['site'] = Site.objects.get(id=self.kwargs['pk'])
        return ctx


class EmailActivateView(DetailView):
    model = EmailActivation
    slug_field = 'code'
    slug_url_kwarg = 'code'

    def get_context_data(self, **kwargs):
        """If can get object, parent recipient enable.
        """
        ctx = super().get_context_data(**kwargs)
        # TODO: This proc is valid place?
        activation = self.get_object()
        activation.recipient.enabled = True
        activation.recipient.save()
        ctx['recipient'] = activation.recipient
        ctx['site'] = activation.recipient.site
        return ctx


# TODO: Set message?
class EmailDeactivateView(DetailView):
    model = EmailDeactivation
    slug_field = 'code'
    slug_url_kwarg = 'code'

    def get(self, request, *args, **kwargs):
        deactivation = self.get_object()
        deactivation.recipient.delete()
        # TODO: Set redirect for user state
        return HttpResponseRedirect(
            reverse_lazy('notifications:email-deactivate-complete'))


# TODO: Not need, if redirection for user state
class EmailDeactivateCompleteView(TemplateView):
    template_name = 'notifications/emaildeactivate_complete.html'


class SlackRecipientListView(LoginRequiredMixin, ListView):
    model = SlackRecipient

    def get_queryset(self):
        qs_ = super().get_queryset()
        return qs_.filter(site_id=self.kwargs['pk'])

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['site'] = Site.objects.get(id=self.kwargs['pk'])
        return ctx


# TODO: Set message
class SlackRecipientCreateView(LoginRequiredMixin, FormMixin, DetailView):
    model = Site
    form_class = SlackRecipientCreateForm
    template_name = 'notifications/slackrecipient_form.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['site'] = self.object
        return initial

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            recipient = form.instance
            recipient.created_by = request.user
            recipient.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'sites:detail', args=(self.object.id,))


class SlackRecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = SlackRecipient
    form_class = SlackRecipientDeleteForm

    def delete(self, request, *args, **kwargs):
        recipient = self.get_object()
        if not recipient.can_delete(request.user):
            return self.get(request, *args, **kwargs)
        resp = super().delete(request, *args, **kwargs)
        # TODO: Need transration
        messages.add_message(
            request, messages.INFO, f"Deleted slack-recipient")
        return resp

    def get_success_url(self):
        recipient = self.get_object()
        return reverse_lazy('sites:detail', args=(recipient.site.id, ))
