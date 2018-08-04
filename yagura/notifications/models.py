from uuid import uuid4

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

    class Meta:
        unique_together = (
            ('site', 'email'),
        )


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
