

import click

from peewee import create_model_tables

from osp.citations.models import Text
from osp.citations.models import Citation


@click.group()
def cli():
    pass


@cli.command()
def init_db():

    """
    Create the database tables.
    """

    create_model_tables([
        Text,
        Citation,
    ], fail_silently=True)


@cli.command()
def ingest_hlom():

    """
    Ingest HLOM texts.
    """

    Text.ingest_hlom()


@cli.command()
def ingest_jstor():

    """
    Ingest JSTOR texts.
    """

    Text.ingest_jstor()
