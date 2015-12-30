

import click

from osp.common.config import config
from osp.corpus.models import Document_Index
from blessings import Terminal


@click.group()
def cli():
    pass


@cli.command()
def create():

    """
    Create the index.
    """

    Document_Index.es_create()


@cli.command()
def delete():

    """
    Delete the index.
    """

    Document_Index.es_delete()


@cli.command()
def reset():

    """
    Reset the index.
    """

    Document_Index.es_reset()


@cli.command()
def count():

    """
    Count documents.
    """

    click.echo(Document_Index.es_count())


@cli.command()
def insert():

    """
    Index documents.
    """

    Document_Index.es_insert()
