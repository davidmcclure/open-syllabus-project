

import click

from osp.common.utils import query_bar
from osp.locations.models.doc_inst import Document_Institution
from osp.locations.jobs.locate import locate
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
def queue_matching():

    """
    Queue institution matching tasks in the worker.
    """

    queue = Queue(connection=redis)

    for doc in query_bar(Document.select()):
        queue.enqueue(locate, doc.id)
