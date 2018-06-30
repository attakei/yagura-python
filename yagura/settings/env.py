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

# System
DEBUG = env('DEBUG')
SECRET_KEY = env('SECRET_KEY')
DATABASES = {
    'default': env.db(),
}

# django-registration
ACCOUNT_ACTIVATION_DAYS = env.int('YAGURA_ACTIVATION_DAYS', default=7)

# Yagura app
YAGURA_BASE_URL = env.url('YAGURA_BASE_URL', 'http://localhost:8000')
YAGURA_DEMO = env('YAGURA_DEMO', default=False)
