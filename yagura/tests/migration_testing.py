# flake8: noqa
from yagura.settings.base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/db.sqlite3',
    }
}
