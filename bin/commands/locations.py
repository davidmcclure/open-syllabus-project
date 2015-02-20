

import os
import click
import csv

from osp.common.models.base import pg_remote, redis
from osp.common.overview import Overview
from osp.common.utils import query_bar, grouper
from osp.locations.models.doc_inst import Document_Institution
from osp.locations.jobs.locate import queue_locate
from osp.locations import queries
from osp.institutions.models.institution import Institution
from osp.corpus.corpus import Corpus
from osp.corpus.models.document import Document
from rq import Queue
from peewee import *


@click.group()
def cli():
    pass


@cli.command()
def init_db():

    """
    Create the database tables.
    """

    pg_remote.connect()

    pg_remote.create_tables([
        Document_Institution
    ], safe=True)


@cli.command()
def queue_location_matching():

    """
    Queue institution matching tasks in the worker.
    """

    queue = Queue(connection=redis)
    queue.enqueue(queue_locate)


@cli.command()
@click.option('--page_len', default=1000)
def push_document_objects(page_len):

    """
    Write document objects into Overview.
    """

    ov = Overview.from_env()

    # Wrap the query in a progress bar.
    query = query_bar(queries.document_objects())

    for group in grouper(query, page_len):

        objects = []
        for d2i in group:
            objects.append([d2i.did, d2i.iid])

        ov.post_document_objects(objects)
