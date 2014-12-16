

import os
import click

from osp.common.models.base import database
from osp.corpus.models.document import Document
from osp.corpus.corpus import Corpus
from rq import Queue
from redis import StrictRedis


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
def queue_document_registration():

    """
    Queue jobs to insert documents in the database.
    """

    # TODO: ENV-ify.
    queue = Queue(connection=StrictRedis())
    corpus = Corpus(os.environ['OSP_CORPUS'])

    for syllabus in corpus.syllabi():
        print(syllabus.relative_path)
