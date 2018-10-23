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


``YAGURA_MAX_TRY_IN_MONITOR``
-----------------------------

:Default: ``1``

Max number trying when monitoring job is failure.

When it is set '1', monitoring job does not retry, return NG immediately.

When it is more than, repeat until rearch value, return last reason with NG.
