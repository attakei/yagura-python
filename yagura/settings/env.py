"""Settings for dependent by environments

Inherit base, and override primary variables to use environment.
At default, docker image use this settings instead of base.
If you want to lock variables without use this,
plese specify DJANGO_SETTINGS_MODULE in environment.
"""
import environ

from yagura.settings.base import *

root = environ.Path(__file__) - 3
env = environ.Env(
    DEBUG=(bool, False),
)
env.read_env(root('.env'))

# System
DEBUG = env('DEBUG')
SECRET_KEY = env('SECRET_KEY')
ALLOWED_HOSTS += env('ALLOWED_HOSTS', default='').split()

DATABASES = {
    'default': env.db(),
}
DEFAULT_FROM_EMAIL = env('EMAIL_FROM', default=DEFAULT_FROM_EMAIL)
EMAIL_CONFIG = env.email_url()
vars().update(EMAIL_CONFIG)

# django-crontab
CRONTAB_DJANGO_SETTINGS_MODULE = env('DJANGO_SETTINGS_MODULE')

# django-registration
ACCOUNT_ACTIVATION_DAYS = env.int('YAGURA_ACTIVATION_DAYS', default=7)

# social-auth-app-django
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY', default=None)
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET', default=None)

# Yagura app
YAGURA_BASE_URL = env('YAGURA_BASE_URL', default='http://localhost:8000')
YAGURA_DEMO = env('YAGURA_DEMO', default=False)
YAGURA_ENABLE_PASSWORD_REGISTRATION = env.bool(
    'YAGURA_ENABLE_PASSWORD_REGISTRATION', default=True)
