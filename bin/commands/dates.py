

import click
import math

from osp.common.models.base import postgres, redis
from osp.common.utils import paginate_query
from osp.corpus.models.text import Document_Text
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
    TODO: Break out the page-through-all-records logic.
    """

    queue = Queue(connection=redis)

    query = (
        Document_Text
        .select()
        .distinct(Document_Text.document)
        .order_by(
            Document_Text.document,
            Document_Text.created.desc()
        )
    )

    for text in paginate_query(query, n):
        queue.enqueue(ext_semester, text.document)
