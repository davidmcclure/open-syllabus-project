

import click

from osp.dates.models.archive_url import Document_Date_Archive_Url
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
        Document_Date_Archive_Url
    ], fail_silently=True)
