Installation
============


Run in local
------------

Simple usage is to clone project.

.. code-block:: bash

    $ git clone https://gitlab.com/attakei/yagura.git
    $ cd yagura
    $ pip install -r requirements.txt
    $ python manage.py migrate
    $ python manage.py runserver

Montoring jobs is define in crontab by django-crontab.
To add jobs for crontab, call ``python manage.py crontab add``

