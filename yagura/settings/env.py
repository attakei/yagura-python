"""Settings for dependent by environments

Inherit base, and override primary variables to use environment.
At default, docker image use this settings instead of base.
If you want to lock variables without use this,
plese specify DJANGO_SETTINGS_MODULE in environment.
"""
import environ

from yagura.settings.base import *

root = environ.Path(__file__) - 3
