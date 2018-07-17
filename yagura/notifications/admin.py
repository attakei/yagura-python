from django.contrib import admin

from yagura.notifications.models import Activation, Recipient

admin.site.register(Recipient)
admin.site.register(Activation)
