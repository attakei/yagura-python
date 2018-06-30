"""Utils
"""
import os

from django.conf import settings


def get_base_url():
    """Generate base URL for email and request
    """
    key = 'YAGURA_BASE_URL'
    if key in os.environ:
        return os.environ[key]
    elif hasattr(settings, key):
        return getattr(settings, key)
    return 'http://localhost'
