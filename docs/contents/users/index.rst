User structure
==============

Definition of users
-------------------

.. glossary::

    Admin
      Administrator of Yagura application project

    Site owner
      Creator of ``Site`` model in Yagura application.
      In this case, "owner" is not real owner of sites, but creator of model.
    
    User
      Regular account of Yagura application.
      All users of not own created sites are seem to ``user`` .

List of permissions
-------------------

.. csv-table::
    :header: "Role", "Admin", "Site owner", "User"
    :widths: 40, 20, 20, 20

    "Register site", "o", "o", "o"
    "Add notification recipient", "o", "o", "o"
    "Delete all recipient from own site", "o", "o", "x"
    "Delete own registered recipient", "o", "o", "o"
