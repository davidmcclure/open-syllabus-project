

import os
import click

from osp.common.models.base import postgres, redis
from osp.common.overview import Overview
from osp.corpus.corpus import Corpus
from osp.corpus.models.document import Document
from osp.corpus.models.document_format import DocumentFormat
from osp.corpus.models.document_text import DocumentText
from osp.corpus.jobs.read_format import read_format
from osp.corpus.jobs.read_text import read_text
from collections import Counter
from prettytable import PrettyTable
from osp.corpus import queries
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
        Document,
        DocumentFormat,
        DocumentText
    ], safe=True)


@cli.command()
def insert_documents():

    """
    Insert documents in the database.
    """

    for s in Corpus.from_env().cli_syllabi():
        try:
            with postgres.transaction():
                Document.create(path=s.relative_path)
        except: pass


@cli.command()
def pull_overview_ids():

    """
    Copy document ids from Overview.
    """

    id = os.environ['OSP_DOC_SET_ID']
    ov = Overview.from_env()

    for o_doc in ov.stream_documents(id):

        query = (
            Document
            .update(stored_id=o_doc['id'])
            .where(Document.path==o_doc['title'])
        )

        query.execute()


@cli.command()
def format_counts():

    """
    Print a table of file format -> count.
    """

    t = PrettyTable(['File Type', 'Doc Count'])
    t.align = 'l'

    for c in queries.format_counts().naive().iterator():
        t.add_row([c.format, c.count])

    click.echo(t)


@cli.command()
def file_count():

    """
    Print the total number of files.
    """

    corpus = Corpus.from_env()
    click.echo(corpus.file_count)


@cli.command()
def queue_read_format():

    """
    Queue format extraction tasks in the worker.
    """

    queue = Queue(connection=redis)

    for syllabus in Corpus.from_env().cli_syllabi():
        queue.enqueue(read_format, syllabus.path)


@cli.command()
def queue_read_text():

    """
    Queue text extraction tasks in the worker.
    """

    queue = Queue(connection=redis)

    for syllabus in Corpus.from_env().cli_syllabi():
        queue.enqueue(read_text, syllabus.path)
