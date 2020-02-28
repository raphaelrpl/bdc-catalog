#
# This file is part of Brazil Data Cube Database module.
# Copyright (C) 2019 INPE.
#
# Brazil Data Cube Database module is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Define command line utility of Brazil Data Cube Database module."""

import os

import click
from flask import Flask, current_app
from flask.cli import FlaskGroup, with_appcontext
from sqlalchemy_utils.functions import create_database, database_exists

from .ext import BDCDatabase
from .fixtures.cli import fixtures
from .models import db as _db


def create_app():
    """Create internal flask app."""
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI',
                                                           'postgresql://postgres:bdc-scripts2019@localhost:5435/bdcdb_2')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    BDCDatabase(app)

    return app


def create_cli(create_app=None):
    """Define a wrapper to create Flask App in order to attach into flask click.

    Args:
         create_app (function) - Create app factory (Flask)
    """
    def create_cli_app(info):
        if create_app is None:
            info.create_app = None

            app = info.load_app()
        else:
            app = create_app()

        return app

    @click.group(cls=FlaskGroup, create_app=create_cli_app)
    def cli(**params):
        """Command line interface for bdc-db."""
        pass

    return cli


cli = create_cli(create_app=create_app)
cli.add_command(fixtures)


@cli.group()
@with_appcontext
def db():
    """Perform database migrations."""


@db.command()
@with_appcontext
def create_db():
    """Create database. Make sure the variable SQLALCHEMY_DATABASE_URI is set."""
    click.secho('Creating database {0}'.format(_db.engine.url),
                fg='green')
    if not database_exists(str(_db.engine.url)):
        create_database(str(_db.engine.url))

    click.secho('Creating extension postgis...', fg='green')
    with _db.session.begin_nested():
        _db.session.execute('CREATE EXTENSION IF NOT EXISTS postgis')

    _db.session.commit()



def main(as_module=False):
    """Create and execute bdc_db as python module."""
    import sys
    cli.main(args=sys.argv[1:], prog_name="python -m bdc_db" if as_module else None)
