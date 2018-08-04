from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import FormMixin
from templated_email import send_templated_mail

from yagura.notifications.forms import AddNotificationForm
from yagura.notifications.models import EmailActivation, EmailDeactivation, EmailRecipient
from yagura.sites.models import Site
from yagura.utils import get_base_url


class AddNotificationView(LoginRequiredMixin, FormMixin, DetailView):
    model = Site
    form_class = AddNotificationForm
    template_name = 'notifications/recipient_form.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['site'] = self.object
        return initial

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        activation = EmailActivation.generate_code(form.instance)
        send_templated_mail(
            template_name='notifications/confirm_recipient',
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


class NotificationDeleteView(LoginRequiredMixin, DetailView):
    model = EmailRecipient
    template_name = 'notifications/recipient_confirm_delete.html'

    def post(self, request, *args, **kwargs):
        recipient = self.get_object()
        deactivation = EmailDeactivation.generate_code(recipient)
        send_templated_mail(
            template_name='notifications/recipient_confirm_delete',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient.email],
            context={
                'site': recipient.site,
                'recipient': recipient,
                'deactivation': deactivation,
                'base_url': get_base_url(),
            }
        )
        return HttpResponseRedirect(
            reverse_lazy('notifications:delete-complete'))


class NotificationDeleteCompleteView(LoginRequiredMixin, TemplateView):
    template_name = 'notifications/recipient_complete_delete.html'


class NotificationListView(LoginRequiredMixin, ListView):
    model = EmailRecipient

    def get_queryset(self):
        qs_ = super().get_queryset()
        return qs_.filter(site_id=self.kwargs['pk'])

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['site'] = Site.objects.get(id=self.kwargs['pk'])
        return ctx


class ActivateView(DetailView):
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


class DeactivateView(DetailView):
    model = EmailDeactivation
    slug_field = 'code'
    slug_url_kwarg = 'code'

    def get(self, request, *args, **kwargs):
        deactivation = self.get_object()
        deactivation.recipient.delete()
        return HttpResponseRedirect(
            reverse_lazy('notifications:deactivate-complete'))


class DeactivateCompleteView(TemplateView):
    template_name = 'notifications/emaildeactivate_complete.html'
