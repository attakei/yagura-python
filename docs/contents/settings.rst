========
Settings
========

Yagura is project based by Django adn third party applications. So, most configuration is conformance with these.

There is following settings Yagura peculiar.

Settings Yagura peciliar
========================

``YAGUA_ENABLE_PASSWORD_REGISTRATION``
--------------------------------------

Default: ``True``

When set ``True`` , use ``django-registration`` and show views, urlpatterns.

If you want registration by only social account, please set ``False`` .
Login form of admin-site is always valiabled no matter whether this value.
