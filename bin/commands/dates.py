

import click

from osp.common.utils import query_bar
from osp.corpus.models.document import Document
from osp.dates.models.archive_url import Document_Date_Archive_Url
from osp.dates.jobs.ext_archive_url import ext_archive_url
from peewee import create_model_tables
from osp.common.models.base import redis
from rq import Queue


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


@cli.command()
def queue_archive_url():

    """
    Queue Internet Archive timestamp extraction tasks in the worker.
    """

    queue = Queue(connection=redis)

    for doc in query_bar(Document.select()):
        queue.enqueue(ext_archive_url, doc.id)
