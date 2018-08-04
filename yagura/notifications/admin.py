from django.contrib import admin

from yagura.notifications.models import EmailActivation, EmailRecipient

admin.site.register(EmailRecipient)
admin.site.register(EmailActivation)
