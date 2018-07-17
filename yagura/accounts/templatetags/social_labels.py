from django import template
from django.utils.translation import gettext_lazy as _

register = template.Library()

SOCIALS = {
    'google-oauth2': {
        'title': _('Google account'),
    }
}


@register.filter
def social_title(value):
    if value not in SOCIALS:
        return value
    return SOCIALS[value]['title']
