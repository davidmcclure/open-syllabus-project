

import os
import click

from osp.common.models.base import database
from osp.common.overview import Overview
from osp.corpus.models.document import Document
from osp.corpus.corpus import Corpus
from collections import Counter
from prettytable import PrettyTable
from clint.textui import progress


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
def pull_overview_ids():

    """
    Copy document ids from Overview.
    """

    id = os.environ['OSP_DOC_SET_ID']
    ov = Overview.from_env()

    for o_doc in ov.list_documents(id).json()['items']:

        # Get the local document row.
        e_doc = Document.get(Document.path==o_doc['title'])

        # Write the Overview id.
        e_doc.stored_id = o_doc['id']
        e_doc.save()


@cli.command()
def file_type_counts():

    """
    Print a list of file type -> count.
    """

    corpus = Corpus.from_env()
    size = corpus.file_count

    click.echo('Reading mime types...')

    counts = Counter()
    for s in progress.bar(corpus.syllabi(), expected_size=size):
        counts[s.libmagic_file_type] += 1

    t = PrettyTable(['Mime Type', 'Doc Count'])
    t.align['Mime Type'] = 'l'

    for mime, count in counts.most_common():
        t.add_row([mime.decode('utf-8'), count])

    click.echo(t)


@cli.command()
def file_count():

    """
    Print the total number of files.
    """

    corpus = Corpus.from_env()
    click.echo(corpus.file_count)
