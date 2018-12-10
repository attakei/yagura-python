"""Custom filter to generate URL
"""
import re

from django import template

register = template.Library()

URL_REGEXP = re.compile(
    r'(?P<scheme>https?)://(?P<user>.+):(?P<pass>.+)@(?P<url>.+)')


@register.filter
def safe_url(value):
    """Mask user and password from URL with Basic Authentication
    """
    m = URL_REGEXP.match(value)
    if not m:
        return value
    return f'{m.group("scheme")}://????:????@{m.group("url")}'
