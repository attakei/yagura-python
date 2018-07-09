from django.contrib import admin

from yagura.notifications.models import Activation, ExtraRecipient

admin.site.register(ExtraRecipient)
admin.site.register(Activation)
