..
    This file is part of Brazil Data Cube Database module.
    Copyright (C) 2019 INPE.

    Brazil Data Cube Database module is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


Running BDC-DB in the Command Line
==================================


Creating the Brazil Data Cube data model
----------------------------------------

**1.** Create a PostgreSQL database and enable the PostGIS extension:

.. code-block:: shell

        SQLALCHEMY_DATABASE_URI="postgresql://username:password@localhost:5432/bdcdb" \
        bdc-db db create-db


**2.** After that, run Flask-Migrate command to prepare the Brazil Data Cube data model:

.. code-block:: shell

        SQLALCHEMY_DATABASE_URI="postgresql://username:password@localhost:5432/bdcdb" \
        bdc-db alembic upgrade


**3.** Load default fixtures of Brazil Data Cube data model:

.. code-block:: shell

        SQLALCHEMY_DATABASE_URI="postgresql://username:password@localhost:5432/bdcdb" \
        bdc-db fixtures init


Updating an Existing Data Model
-------------------------------

In order to make changes to the models of a module, we need to create a new alembic revision.
To make sure that database is up to date, use the following:

.. code-block:: shell

        SQLALCHEMY_DATABASE_URI="postgresql://username:password@localhost:5432/bdcdb" \
        bdc-db alembic upgrade heads


Updating the Migration Scripts
------------------------------

The ``bdc-db`` supports ``alembic`` branches, which enables to generate revisions on different modules.

Each module should create a ``branch`` for its revisions. The following example describes how to create a revision directly on ``bdc-db``:

.. code-block:: shell

        SQLALCHEMY_DATABASE_URI="postgresql://username:password@localhost:5432/bdcdb" \
        bdc-db alembic revision "Revision message."

It creates a new revision and it will be placed in the ``bdc_db/alembic``.

To create a new revision for module, you must create a `branch <https://alembic.sqlalchemy.org/en/latest/branches.html>`_ and get latest revision id to make persistent migration.
Use the following command to get latest revision id:

.. code-block:: shell

        SQLALCHEMY_DATABASE_URI="postgresql://username:password@localhost:5432/bdcdb" \
        bdc-db alembic heads

The result will be something like that:

.. code-block:: console

        4a2287967b77 -> c7b452f40e8c (default) (head), empty message.


In this example, the latest ``revision id`` is ``c7b452f40e8c``.

In order to do generate migration for your module, use the following command:

.. code-block:: shell

        SQLALCHEMY_DATABASE_URI="postgresql://username:password@localhost:5432/bdcdb" \
        bdc-db alembic revision "Revision message." \
            --path your_module_name/alembic \
            --branch your_module_name \
            --parent c7b452f40e8c


.. note::

        When a ``parent`` is not given for **other modules** the revision will be placed into default branch ``()`` and you may face issues
        during ``bdc-db alembic upgrade``.
        If the path is not given the new revision will be placed in the ``bdc_db/alembic`` directory and should be moved.