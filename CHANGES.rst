===========
Change logs
===========

ver 0.9.1
=========

:Date: 2018-11-07

Features
--------

* Render class name into reason when raised aiohttp.ClientError

Fixes
-----

* Adjust new version of aioresponses

ver 0.9.0
=========

:Date: 2018-10-23

Features
--------

* Can retry in monitoring if failure (``settings``)

Fixes
-----

* Enable testings for async functions

ver 0.8.3
=========

:Date: 2018-09-30

Fixes
-----

* In site-list, split template to site overview
* Show email list in emailrecipient-list view
* Change layout of site overview in site list
* Remove ``theme.css`` (this is for bootstrap3 not 4)
* Rename ``custom.css`` to ``layout.css``

ver 0.8.2
=========

:Date: 2018-09-28

Fixes
-----

* Fix templates for ``django-registration``

ver 0.8.1
=========

:Date: 2018-09-14

Fixes
-----

* Remove ``intial`` fixture and merge into ``unittest_suite``

ver 0.8
=======

:Date: 2018-09-08

Features
--------

* Define CLI command

Fixes
-----

* Lock version of ``django-registration`` (more than 3.0)


ver 0.7.1
=========

:Date: 2018-08-26

Features
--------

* Monitor websites by async in running task

Fixes
-----

* Adjust all layouts to render navbar always
* Fix CI/CD pipeline
* Fix typo in upgrade guide

ver 0.7.0
=========

:Date: 2018-08-26

Fixes
-----

* Change auth user model(breaking change)
* Docker image contains only installed packages


ver 0.6.0
=========

:Date: 2018-08-23

Features
--------

* Can registr notification recipient by any users

Fixes
-----

* Define default login error URL
* Fix layouts of navbar and footer


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

