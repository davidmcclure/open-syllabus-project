

import os
import click
import csv

from osp.common.models.base import database
from osp.common.overview import Overview
from osp.locations.models.doc_inst import DocInst
from osp.locations.jobs.locate import locate
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

    database.connect()
    database.create_tables([DocInst])


@cli.command()
def queue_location_matching():

    """
    Queue institution matching tasks in the worker.
    """

    # TODO: ENV-ify.
    queue = Queue(connection=StrictRedis())

    for syllabus in Corpus.from_env().cli_syllabi():
        queue.enqueue(locate, syllabus.path)


@cli.command()
@click.option('--page', default=50)
def write_document_objects(page):

    """
    Write document objects into Overview.
    """

    ov = Overview.from_env()

    iid = Institution.stored_id.alias('iid')
    did = Document.stored_id.alias('did')

    query = (
        DocInst
        .select(iid, did)
        .join(Institution)
        .join(Document, on=(DocInst.document==Document.path))
        .where(~(Document.stored_id >> None))
        .distinct([DocInst.document])
        .order_by(DocInst.document, DocInst.created.desc())
    )

    objects = []
    for d2i in query.naive().iterator():
        objects.append([d2i.did, d2i.iid])

    # Write the objects in pages.
    for i in range(0, len(objects), page):
        r = ov.post_document_objects(objects[i:i+page])
