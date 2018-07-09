from django.views.generic import DetailView

from yagura.notifications.models import Activation


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
