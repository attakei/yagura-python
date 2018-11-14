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


``YAGURA_SITES_LIMIT``
----------------------

:Default: `1`

Number of sites that user can add in site.

If it is set 0, user can add sites unlimitedly.


``YAGURA_MONITOR_FUNC``
-----------------------

:Default: yagura.monitors.services.monitor_site_requests

In monitoring task, call implemented request function.

Currently, accept these methods

* ``yagura.monitors.services.monitor_site_requests``

  * ``requests`` based HTTP call **(recommended)**
  * Is stable, but process time increase monotonically by num of monitoring websites

* ``yagura.monitors.services.monitor_site_aiohttp``

  * ``aiohttp`` based HTTP call
  * Process time is shorter tendency than ``requests`` , but unstable.


``YAGURA_ENABLE_DELETING_SITES``
--------------------------------

:Default: True

Enable delete site by user registered.

If you want to disable monitoring but not want to delete logs. Set ``False``
