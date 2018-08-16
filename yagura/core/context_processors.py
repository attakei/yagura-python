from django.conf import settings

from yagura import __version__


def yagura_version(request):
    return {
        'YAGURA_VERSION': __version__
    }


def yagura_conf(request):
    return {
        'ENABLE_PASSWORD_REGISTRATION':
            settings.YAGURA_ENABLE_PASSWORD_REGISTRATION,
    }
