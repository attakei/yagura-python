"""Local development and debugging settings
"""
from yagura.settings.base import *

# Enforce debug mode
DEBUG = True

# Use django-debug-toolbar
if 'django.contrib.staticfiles' not in INSTALLED_APPS:
    INSTALLED_APPS += [
        'django.contrib.staticfiles',
    ]
INSTALLED_APPS += [
    'debug_toolbar',
]
MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]
INTERNAL_IPS = [
    '127.0.0.1',
]
