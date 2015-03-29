

import click

from osp.common.config import config
from osp.corpus.models.document import Document
from osp.locations.models.doc_inst import Document_Institution
from osp.locations.jobs.match_doc import match_doc
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
        Document_Institution,
    ], fail_silently=True)


@cli.command()
def queue_match_doc():

    """
    Queue institution matching tasks in the worker.
    """

    for doc in Document.select():
        config.rq.enqueue(match_doc, doc.id)
