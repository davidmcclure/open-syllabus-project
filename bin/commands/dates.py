

import click
import math

from osp.common.models.base import postgres, redis
from osp.common.utils import paginate_query
from osp.corpus.queries import all_document_texts
from osp.dates.semester.models.semester import Document_Semester
from osp.dates.semester.jobs.ext_semester import ext_semester
from rq import Queue


@click.group()
def cli():
    pass


@cli.command()
def init_db():

    """
    Create the database tables.
    """

    postgres.connect()

    postgres.create_tables([
        Document_Semester
    ], safe=True)


@cli.command()
@click.option('--n', default=10000)
def queue(n):

    """
    Queue semester extraction queries.
    """

    queue = Queue(connection=redis)

    for text in paginate_query(all_document_texts(), n):
        queue.enqueue(ext_semester, text.document)
