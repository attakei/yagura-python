from django.db import models
from django.utils.timezone import now

from yagura.sites.models import Site

WEBSITE_STATE_CHOICES = (
    ('OK', 'OK'),
    ('NG', 'NG'),
)


class StateHistory(models.Model):
    """State history per sites
    """
    site = models.ForeignKey(
        Site, on_delete=models.CASCADE, related_name='states')
    state = models.CharField(
        'State label', max_length=10, choices=WEBSITE_STATE_CHOICES)
    reason = models.TextField('Reason of state', default='')
    begin_at = models.DateTimeField(default=now)
    end_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)

    class Meta:
        unique_together = (
            ('site', 'begin_at', ),
        )
        ordering = ['begin_at']
