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


**2.** After that, run Flask-Alembic command to prepare the Brazil Data Cube data model:

.. code-block:: shell

        SQLALCHEMY_DATABASE_URI="postgresql://username:password@localhost:5432/bdcdb" \
        bdc-db alembic upgrade


Updating an Existing Data Model
-------------------------------

In order to make changes to the models of a module, we need to create a new alembic revision.
To make sure that database is up to date, use the following:

.. code-block:: shell

        SQLALCHEMY_DATABASE_URI="postgresql://username:password@localhost:5432/bdcdb" \
        bdc-db alembic upgrade heads


Updating the Migration Scripts
------------------------------

.. code-block:: shell

        SQLALCHEMY_DATABASE_URI="postgresql://username:password@localhost:5432/bdcdb" \
        bdc-db alembic revision "Revision message."


Loading Demo Data
-----------------

Load default fixtures of Brazil Data Cube data model:

.. code-block:: shell

        SQLALCHEMY_DATABASE_URI="postgresql://username:password@localhost:5432/bdcdb" \
        bdc-db fixtures init



Adding bdc-db as dependency to existing modules
-----------------------------------------------

.. note::

        The following steps assume that ``bdc-test`` is the name of the module for which you are adding alembic support.


The module ``bdc-db`` uses dynamic model loading in order to track both ``bdc-db`` and others python modules. It was built on top of `Python Setup entry_points <https://setuptools.readthedocs.io/en/latest/setuptools.html>`_.

In order to load models dynamically, you must edit ``setup.py`` in your package ``bdc-test`` and append your module ``alembic`` and ``models`` to the following entry points:


- **bdc_db.alembic** defines where migrations will be stored.
- **bdc_db.models** defines where SQLAlchemy models will be mapped.


The ``setup.py`` should be like as follows:

.. code-block:: python

        setup(
          ...,

          entry_points={
            'bdc_db.alembic': [
                'bdc_test = bdc_test:alembic'
            ],
            'bdc_db.models': [
                'bdc_test = bdc_test.models'
            ]
          },
        )


This will register the ``bdc_test/alembic`` directory in the alembic's version locations.
It also will make the ``bdc_test/models`` be discoverable and loaded in memory to track alembic revisions.


Creating a new revision
-----------------------

The ``bdc-db`` supports `Alembic Branches <https://alembic.sqlalchemy.org/en/latest/branches.html>`_, which enables to generate revisions on different modules.

To create a new revision for module ``bdc_test``, you must create a ``branch`` and get latest revision id to make persistent migration.
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
        The ``--parent`` argument is required only in the first revision generation.
        If the path is not given the new revision will be placed in the ``bdc_db/alembic`` directory and should be moved.
