"""Settings for Yagura demo site
"""
from yagura.settings.env import *

CRONJOBS = [
    ('5 0 * * SUN', 'django.core.management.call_command', ['cleanup_db']),
    ('*/10 * * * *', 'django.core.management.call_command', ['monitor_all']),
]
