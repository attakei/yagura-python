===============
Upgrading guide
===============

Upgrading for breaking changes

Upgrate to ver 0.7
==================

This version use ``yagura.accounts.models.User`` as authentication user model.

So to upgrade version, need to stop server and run offline migration.

1. Dump back up to edit migration data 
--------------------------------------

Run django command ``dumpdata`` with specifed argument as applications and models to keep prjoject data.
Recommend to set ``auth.user`` and ``yagura.xxx`` apps(sites, monitoring and notifications)

.. code-block:: bash

    $ python manage.py dumpdata auth.user sites monitors notifications > dumpdata.json


2. Edit dumpdata to insert upgraded database
--------------------------------------------

Edit dumpdata to load after upgraded database

* From: ``"model": "auth.user"`` to ``"model": "accouts.user"``

3. Upgrade Yagura
-----------------

4. Clean up database
--------------------

Remove tables from database of backends (if you use SQLite, remove database file)

5. Run migrate and loaddata
---------------------------

Place ``dumpdata.json`` into your fixture directory.
And, migrate database and load dumpdata.

.. code-block:: bash

    $ python manage.py migrate
    $ python manage.py loaddata dumpdata
