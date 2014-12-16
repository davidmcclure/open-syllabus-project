

import os
import click

from osp.common.models.base import database
from osp.common.overview import Overview
from osp.corpus.models.document import Document
from osp.corpus.corpus import Corpus


@click.group()
def cli():
    pass


@cli.command()
def init_db():

    """
    Create the database tables.
    """

    database.connect()
    database.create_tables([Document])


@cli.command()
def insert_documents():

    """
    Insert documents in the database.
    """

    docs = []
    for syllabus in Corpus.from_env().syllabi():
        docs.append({'path': syllabus.relative_path})

    with database.transaction():
        Document.insert_many(docs).execute()


@cli.command()
def write_overview_ids():

    """
    Copy document ids from Overview.
    """

    ov = Overview.from_env()

    for o_doc in ov.list_documents(5).json()['items']:

        # Get the local document row.
        e_doc = Document.get(Document.path==o_doc['title'])

        # Write the Overview id.
        e_doc.stored_id = o_doc['id']
        e_doc.save()
