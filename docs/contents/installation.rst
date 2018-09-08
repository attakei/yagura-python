=============
Getting start
=============

Initialize project
==================


Use CLI
-------

Yagura deliver command line tool.

.. code-block:: bash

    $ pip install yagura
    $ yagura init yourproject


Run cloned source
-----------------

Project source has all running code.

.. code-block:: bash

    $ git clone https://gitlab.com/attakei/yagura.git yagura


Start server
============

.. code-block:: bash

    $ cd /pat/to/yourproject
    $ pip install -r requirements.txt
    $ python manage.py migrate
    $ python manage.py runserver

Montoring jobs is define in crontab by django-crontab.
To add jobs for crontab, call ``python manage.py crontab add``

