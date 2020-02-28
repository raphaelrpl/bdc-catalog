#
# This file is part of Brazil Data Cube Database module.
# Copyright (C) 2019 INPE.
#
# Brazil Data Cube Database module is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Defines flask extension module for Brazil Data Cube Database."""

import os

import pkg_resources
from flask import Flask, current_app
from flask_alembic import Alembic
from sqlalchemy.orm import configure_mappers

from .models import db


def include_object(object, name, type_, reflected, compare_to):
    """Ignores the tables in 'exclude_tables'"""
    exclude_tables = current_app.config.get('ALEMBIC_EXCLUDE_TABLES', [])

    return not (type_ == "table" and name in exclude_tables)


class BDCDatabase:
    """Brazil Data Cube Database extension."""

    def __init__(self, app=None, **kwargs):
        """Extension initialization."""
        self.alembic = Alembic(run_mkdir=True, command_name='alembic')

        if app:
            self.init_app(app, **kwargs)

    def init_app(self, app: Flask, **kwargs):
        """Initialize flask application object."""
        self.init_db(app, **kwargs)

        script_location = pkg_resources.resource_filename(
            'bdc_db', 'alembic'
        )

        version_locations = [
            (base_entry.name, pkg_resources.resource_filename(
                base_entry.module_name, os.path.join(*base_entry.attrs,)
            )) for base_entry in pkg_resources.iter_entry_points(
                'bdc_db.alembic'
            )
        ]

        if ('bdc_db', script_location) in version_locations:
            version_locations.remove(('bdc_db', script_location))

        # Defines entrypoints for dynamically model loading
        app.config.setdefault('ALEMBIC', {
            'script_location': script_location,
            'version_locations': version_locations,
        })

        print(app.config['ALEMBIC'])

        app.config.setdefault('ALEMBIC_EXCLUDE_TABLES', ['spatial_ref_sys'])

        handler_include_table = kwargs.get('include_object', include_object)

        app.config.setdefault('ALEMBIC_CONTEXT', {
            'compare_type': True,
            'include_schemas': True,
            'include_object': handler_include_table
        })

        # Initialize Flask-Alembic
        self.alembic.init_app(app, **kwargs)

        app.extensions['bdc-db'] = self

    def init_db(self, app: Flask, entry_point_group: str='bdc_db.models', **kwargs):
        """Initialize Flask-SQLAlchemy extension.

        Args:
            app - Flask application
            entry_point_group - Entrypoint definition to load models
            **kwargs - Optional arguments to Flask-SQLAlchemy
        """
        # Setup SQLAlchemy
        app.config.setdefault(
            'SQLALCHEMY_DATABASE_URI',
            os.environ.get('SQLALCHEMY_DATABASE_URI')
        )

        app.config.setdefault(
            'SQLALCHEMY_TRACK_MODIFICATIONS',
            os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS', False)
        )
        app.config.setdefault('SQLALCHEMY_ECHO', False)

        # Initialize Flask-SQLAlchemy extension.
        database = kwargs.get('db', db)
        database.init_app(app)

        # Loads all models
        if entry_point_group:
            for base_entry in pkg_resources.iter_entry_points(entry_point_group):
                base_entry.load()

        # All models should be loaded by now.
        configure_mappers()