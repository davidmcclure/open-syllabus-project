

import click

from osp.fields.models.field import Field
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
        Field,
    ], fail_silently=True)
