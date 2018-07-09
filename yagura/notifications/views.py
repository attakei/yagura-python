from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from templated_email import send_templated_mail

from yagura.notifications.forms import AddNotificationForm
from yagura.notifications.models import Activation
from yagura.sites.models import Site
from yagura.utils import get_base_url


class AddNotificationView(FormMixin, DetailView):
    model = Site
    form_class = AddNotificationForm
    template_name = 'notifications/extrarecipient_form.html'

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
        # TODO: Verify by test code
        form.save()
        activation = Activation.generate_code(form.instance)
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


class ActivateView(DetailView):
    model = Activation
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
