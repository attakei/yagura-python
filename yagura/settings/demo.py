"""Settings for Yagura demo site
"""
from yagura.settings.env import *

# Override authentication backend settings
AUTHENTICATION_BACKENDS = (
    # From social-auth-app-django
    'social_core.backends.google.GoogleOAuth2',
    # Default backend
    'django.contrib.auth.backends.ModelBackend',
)

CRONJOBS = [
    ('5 0 * * SUN', 'django.core.management.call_command', ['cleanup_db']),
    ('*/10 * * * *', 'django.core.management.call_command', ['monitor_all']),
]
