from django.conf import settings


def yagura_conf(request):
    return {
        'ENABLE_PASSWORD_REGISTRATION':
            settings.YAGURA_ENABLE_PASSWORD_REGISTRATION,
    }
