

import os
import click
import csv

from osp.common.models.base import database
from osp.common.overview import Overview
from osp.locations.models.doc_to_inst import DocToInst
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
    database.create_tables([DocToInst])


@cli.command()
def queue_location_matching():

    """
    Queue institution matching tasks in the worker.
    """

    # TODO: ENV-ify.
    queue = Queue(connection=StrictRedis())

    for syllabus in Corpus.from_env().syllabi():
        queue.enqueue(locate, syllabus.path)


@cli.command()
@click.option('--page', default=50)
def write_document_objects(page):

    """
    DEV: Write document objects into Overview.
    """

    ov = Overview.from_env()

    iid = Institution.stored_id.alias('iid')
    did = Document.stored_id.alias('did')

    query = (
        DocToInst
        .select(iid, did)
        .join(Institution)
        .join(Document, on=(DocToInst.document==Document.path))
        .where(~(Document.stored_id >> None))
        .distinct([DocToInst.document])
        .order_by(DocToInst.document, DocToInst.created.desc())
    )

    objects = []
    for d2i in query.naive().iterator():
        objects.append([d2i.did, d2i.iid])

    # Write the objects in pages.
    for i in range(0, len(objects), page):
        r = ov.post_document_objects(objects[i:i+page])


@cli.command()
@click.argument('out_path', type=click.Path())
def make_csv(out_path):

    """
    DEV: Generate a CSV file.

    :param in_file: A path for the new CSV file.
    """

    out_file = open(out_path, 'w')

    # CSV writer:
    cols = ['document', 'longitude', 'latitude']
    writer = csv.DictWriter(out_file, cols)

    # Get current doc->inst links.
    current = DocToInst.select_current()

    rows = []
    for doc in current.naive().iterator():

        lonlat = (
            doc.institution.lonlats
            .order_by(LonLat.created.desc())
            .first()
        )

        rows.append({
            'document': doc.document,
            'latitude': lonlat.lat,
            'longitude': lonlat.lon
        })

    writer.writeheader()
    writer.writerows(rows)
