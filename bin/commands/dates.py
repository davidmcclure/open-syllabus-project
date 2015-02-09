

import click
import math

from osp.common.models.base import pg_local, redis
from osp.common.utils import paginate_query
from osp.corpus.queries import all_document_texts
from osp.dates.semester.models.semester import Document_Semester
from osp.dates.semester.jobs.ext_semester import ext_semester
from osp.dates.semester import queries
from prettytable import PrettyTable
from rq import Queue


@click.group()
def cli():
    pass


@cli.command()
def init_db():

    """
    Create the database tables.
    """

    pg_local.connect()

    pg_local.create_tables([
        Document_Semester
    ], safe=True)


@cli.command()
@click.option('--n', default=10000)
def queue(n):

    """
    Queue semester extraction queries.
    """

    queue = Queue(connection=redis)
    pages = paginate_query(all_document_texts(), n)

    for page in pages:
        for text in page.iterator():
            queue.enqueue(ext_semester, text.document)


@cli.command()
def semester_counts():

    """
    Print a table of semester -> count.
    """

    t = PrettyTable(['Year', 'Semester', 'Doc Count'])
    t.align = 'l'

    for c in queries.semester_counts().naive().iterator():
        t.add_row([c.year, c.semester, c.count])

    click.echo(t)
