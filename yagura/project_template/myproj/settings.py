"""My project settings module

At default, inherit from recommended and defualt settings(yagura.settings.base)

"""
import os
from pathlib import Path

from yagura.settings.base import *

BASE_DIR = Path(__file__).resolve().parents[1]


# --------------------------------------
# Yagura settings
#   Configure for your environment
# --------------------------------------
YAGURA_BASE_URL = ''
YAGURA_SITES_LIMIT = 10
YAGURA_ENABLE_PASSWORD_REGISTRATION = True


# --------------------------------------
# Django settings
#   For detail, django documentation
# --------------------------------------
# Domain and hostname
ALLOWED_HOSTS = [
    'localhost',
    # TODO: Add your site domain
]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(BASE_DIR / 'db.sqlite3'),
    }
}

# Email sending
#   If you use other than SMTP settings, please override them
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = ''
EMAIL_PORT = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
DEFAULT_FROM_EMAIL = 'noreply@example.com'

# Localization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'

# Auhtentications
AUTHENTICATION_BACKENDS = (
    # Default backend
    'django.contrib.auth.backends.ModelBackend',
)

# --------------------------------------
# Django core settings
#   You don't have to edit these variables usually
# --------------------------------------
SECRET_KEY = '{secret_key}'

DEBUG = False

ROOT_URLCONF = '{project_name}.urls'
