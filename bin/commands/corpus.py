

import click

from osp.common.models.base import database
from osp.corpus.models.document import Document


@click.group()
def cli():
    pass


@cli.command()
def init_db():

    """
    Create the database tables.
    """

    database.connect()
    database.create_tables([Document])


@cli.command()
def queue_document_registration():

    """
    Queue jobs to insert documents in the database.
    """

    pass
