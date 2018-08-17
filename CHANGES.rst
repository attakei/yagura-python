===========
Change logs
===========

ver 0.5.3
=========

:Date: 2018-08-17

Features
--------

* Add footer to display version

Fixes
-----

* Monitoring request does not follow redirect



ver 0.5.2
=========

:Date: 2018-08-15

Fixes
-----

* Include `.mo` files (compiled messages)

ver 0.5.1
=========

:Date: 2018-08-14

Fixes
-----

* When use ``yagura.settings.env`` , set default values as possible


ver 0.5.0
=========

:Date: 2018-08-12

Features
--------

* Add slack recipient as notification target
* Monitoring function checks HTTP status specified by register user
* Link to target site URL in site detail page
* Remove demo site sources in this project

Fixes
-----

* Use user locale to render datetime


ver 0.4.1
=========

:Date: 2018-07-21

Fixes
-----

* Can't delete notification email (#22)

ver 0.4.0
=========

:Date: 2018-07-19

Features
--------

* Enable social authentication by social-auth-app-django
* Toggle password registration
* Register other notifications for each sites ( not owner emails)
* Can disable limit of monitring sites
* MySQL support in docker container

Fixes
-----

* Split locale file into each applications
* Split template files into each applications
* Move statc resource into ``yagura.core`` application


Ver 0.3.0
=========

:Date: 2018-07-08

**Important!**
This version is not same code base from old version, does not have compatbility.

Features
--------

* Registration by email with activation
* Registration sites from users
* Monitor sites and notify when detect chenged state

  * Notify method is only email
* Simple available i18n

