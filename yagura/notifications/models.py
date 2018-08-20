from uuid import uuid4

from django.conf import settings
from django.db import models

from yagura.sites.models import Site


class EmailRecipient(models.Model):
    """Other email not users

    * Manage per recipient and target site
    """
    site = models.ForeignKey(
        Site, on_delete=models.CASCADE, related_name='recipients')
    email = models.EmailField()
    enabled = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = (
            ('site', 'email'),
        )

    def can_delete(self, user) -> bool:
        """Judge that ``user`` can delete this recipient.
        Each user can delete it

        * Creator of this recipient
        * Creator of this site

        :params user: Target user
        """
        if self.created_by == user:
            return True
        if self.site.created_by == user:
            return True
        return False


class EmailActivation(models.Model):
    """Email-recipient activation code
    """
    recipient = models.ForeignKey(EmailRecipient, on_delete=models.CASCADE)
    code = models.UUIDField()

    @classmethod
    def generate_code(cls, recipient):
        act = cls.objects.create(recipient=recipient, code=uuid4())
        return act


class EmailDeactivation(models.Model):
    """Email-recipient deactivation code
    """
    recipient = models.ForeignKey(EmailRecipient, on_delete=models.CASCADE)
    code = models.UUIDField()

    @classmethod
    def generate_code(cls, recipient):
        inst = cls.objects.create(recipient=recipient, code=uuid4())
        return inst


class SlackRecipient(models.Model):
    """Other notification recipient for Slack Incoming web-hook
    """
    site = models.ForeignKey(
        Site, on_delete=models.CASCADE, related_name='slack_recipients')
    url = models.URLField('Webhook URL')
    channel = models.CharField(
        'Channel name(optional)', max_length=22, null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = (
            ('site', 'url', 'channel'),
        )

    def can_delete(self, user) -> bool:
        """Judge that ``user`` can delete this recipient.
        Each user can delete it

        * Creator of this recipient
        * Creator of this site

        :params user: Target user
        """
        if self.created_by == user:
            return True
        if self.site.created_by == user:
            return True
        return False
