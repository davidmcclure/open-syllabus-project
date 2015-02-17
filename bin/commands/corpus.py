

import os
import click
import csv

from osp.common.config import config
from osp.common.models.base import pg_local, redis
from osp.common.overview import Overview
from osp.common.utils import paginate_query
from osp.corpus.corpus import Corpus
from osp.corpus.models.document import Document
from osp.corpus.models.format import Document_Format
from osp.corpus.models.text import Document_Text
from osp.corpus.jobs.read_format import read_format
from osp.corpus.jobs.read_text import read_text
from osp.corpus import queries
from playhouse.postgres_ext import ServerSide
from collections import Counter
from clint.textui.progress import bar
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
        Document,
        Document_Format,
        Document_Text
    ], safe=True)


@cli.command()
def insert_documents():

    """
    Insert documents in the database.
    """

    segments = Corpus.from_env().segments()
    itr = bar(segments, expected_size=4096)

    for segment in itr:

        rows = []
        for syllabus in segment.syllabi():
            rows.append({'path': syllabus.relative_path})

        with pg_local.transaction():
            Document.insert_many(rows).execute()


@cli.command()
def pull_overview_ids():

    """
    Copy document ids from Overview.
    """

    id = config['overview']['doc_set']
    ov = Overview.from_env()

    for o_doc in ov.stream_documents(id):

        query = (
            Document
            .update(stored_id=o_doc['id'])
            .where(Document.path==o_doc['title'])
        )

        query.execute()


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
@click.argument('out_path', type=click.Path())
@click.option('--frag_len', default=1500)
@click.option('--page_len', default=10000)
def truncated_csv(out_path, frag_len, page_len):

    """
    Write a CSV with truncated document texts.
    """

    out_file = open(out_path, 'w')

    # CSV writer.
    cols = ['id', 'title', 'text']
    writer = csv.DictWriter(out_file, cols)
    writer.writeheader()

    query = Document_Text.select()
    count = query.count()

    for row in bar(query, expected_size=count):

        # Truncate the text.
        fragment = row.text[:frag_len]

        writer.writerow({
            'id': row.document,
            'title': row.document,
            'text': fragment
        })
