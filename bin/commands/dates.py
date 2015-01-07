

import click

from osp.common.models.base import postgres, redis
from osp.dates.models.dateutil_parse import DateutilParse
from osp.dates.jobs.dateutil_parse import dateutil_parse
from osp.dates.queries import document_texts
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
    postgres.create_tables([DateutilParse], safe=True)


@cli.command()
@click.option('--depth', default=500)
def queue_dateutil_parse(depth):

    """
    Queue the dateutil `parse` extractor.
    """

    queue = Queue('dateutil', connection=redis)

    for text in document_texts().naive().iterator():
        queue.enqueue(dateutil_parse, text.document, text.text, depth)
