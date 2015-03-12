

import os
import click
import csv
import sys

from osp.common.models.base import queue
from osp.common.utils import query_bar
from osp.corpus.corpus import Corpus
from osp.corpus.models.document import Document
from osp.corpus.models.format import Document_Format
from osp.corpus.models.text import Document_Text
from osp.corpus.jobs.ext_format import ext_format
from osp.corpus.jobs.ext_text import ext_text
from peewee import create_model_tables
from prettytable import PrettyTable


@click.group()
def cli():
    pass


@cli.command()
def init_db():

    """
    Create the database tables.
    """

    create_model_tables([
        Document,
        Document_Format,
        Document_Text
    ], fail_silently=True)


@cli.command()
def insert_documents():

    """
    Insert documents in the database.
    """

    corpus = Corpus.from_env()
    Document.insert_documents(corpus)


@cli.command()
def queue_format():

    """
    Queue format extraction tasks in the worker.
    """

    for doc in query_bar(Document.select()):
        queue.enqueue(ext_format, doc.id)


@cli.command()
def queue_text():

    """
    Queue text extraction tasks in the worker.
    """

    for doc in query_bar(Document.select()):
        queue.enqueue(ext_text, doc.id)


@cli.command()
def format_counts():

    """
    Print a table of file format -> count.
    """

    t = PrettyTable(['File Type', 'Doc Count'])
    t.align = 'l'

    for c in Document_Format.format_counts():
        t.add_row(c)

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

    for row in query_bar(Document_Text.select()):

        # Truncate the text.
        fragment = row.text[:frag_len]

        writer.writerow({
            'id': row.document,
            'title': row.document,
            'text': fragment
        })
