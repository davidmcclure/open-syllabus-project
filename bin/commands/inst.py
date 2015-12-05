

import click

from osp.institutions.models.institution import Institution
from peewee import create_model_tables


@click.group()
def cli():
    pass


@cli.command()
def init_db():

    """
    Create the database tables.
    """

    create_model_tables([
        Institution,
    ], fail_silently=True)


@cli.command()
def insert_us():

    """
    Insert US institutions.
    """

    Institution.insert_us()
