

import os
import click
import csv

from osp.common.models.base import postgres, redis
from osp.common.overview import Overview
from osp.locations.models.doc_inst import DocInst
from osp.locations.jobs.locate import locate
from osp.locations.queries import document_objects
from osp.institutions.models.institution import Institution
from osp.institutions.models.lonlat import LonLat
from osp.corpus.corpus import Corpus
from osp.corpus.models.document import Document
from rq import Queue
from redis import StrictRedis
from peewee import *


@click.group()
def cli():
    pass


@cli.command()
def init_db():

    """
    Create the database tables.
    """

    postgres.connect()
    postgres.create_tables([DocInst], safe=True)


@cli.command()
def queue_location_matching():

    """
    Queue institution matching tasks in the worker.
    """

    queue = Queue(connection=redis)

    for syllabus in Corpus.from_env().cli_syllabi():
        queue.enqueue(locate, syllabus.path)


@cli.command()
@click.option('--page', default=50)
def write_document_objects(page):

    """
    Write document objects into Overview.
    """

    ov = Overview.from_env()

    objects = []
    for d2i in document_objects().naive().iterator():
        objects.append([d2i.did, d2i.iid])

    # Write the objects in pages.
    for i in range(0, len(objects), page):
        ov.post_document_objects(objects[i:i+page])
