from django.db import models

from yagura.sites.models import Site


class ExtraRecipient(models.Model):
    """Other recipients not users

    * Manage per recipient and target site
    """
    site = models.ForeignKey(
        Site, on_delete=models.CASCADE, related_name='extra_recipients')
    email = models.EmailField()
    enabled = models.BooleanField(default=False)

    class Meta:
        unique_together = (
            ('site', 'email'),
        )
