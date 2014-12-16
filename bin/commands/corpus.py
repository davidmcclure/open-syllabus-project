

import os
import click

from osp.common.models.base import database
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
