======
Yagura
======


.. image:: https://img.shields.io/pypi/v/yagura.svg
   :alt: PyPI - Version
   :target: https://pypi.org/project/yagura/

.. image:: https://img.shields.io/pypi/l/Yagura.svg
   :alt: PyPI - License
   :target: https://pypi.org/project/yagura/

.. image:: https://gitlab.com/attakei/yagura/badges/master/pipeline.svg
   :alt: GitLab-CI pipeline
   :target: https://gitlab.com/attakei/yagura/pipelines


Simple site monitoring web-app for small team.


Description
===========

Yagura is simple website monitoring kit based by Django framework.
Yagura provides website monitorings, alerts and status reportings.


Features
========

* Health-check report of websites
* Notify state changing by email and Slack webhook


Try demo
========

See https://yagura.herokuapp.com


Latest changes
==============

:Date: 2018-09-30

Fixes
-----

* In site-list, split template to site overview
* Show email list in emailrecipient-list view
* Change layout of site overview in site list
* Remove ``theme.css`` (this is for bootstrap3 not 4)
* Rename ``custom.css`` to ``layout.css``


Initial user
============

(Not work demo site)

* Username: ``admin``
* Password: ``Yagura!!``
