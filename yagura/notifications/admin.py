from django.contrib import admin

from yagura.notifications.models import (
    EmailActivation, EmailRecipient, SlackRecipient
)

admin.site.register(EmailRecipient)
admin.site.register(EmailActivation)
admin.site.register(SlackRecipient)
