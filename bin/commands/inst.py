

import click

from osp.institutions.models.institution import Institution
from osp.institutions.models.institution_document import Institution_Document
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
        Institution_Document,
    ], fail_silently=True)


@cli.command()
def insert_us():

    """
    Insert US institutions.
    """

    Institution.insert_us()


@cli.command()
def insert_uk():

    """
    Insert UK institutions.
    """

    Institution.insert_uk()
