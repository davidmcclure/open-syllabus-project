

import os
import click

from osp.common.models.base import database
from osp.common.overview import Overview
from osp.corpus.models.document import Document
from osp.corpus.corpus import Corpus
from collections import Counter
from prettytable import PrettyTable


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

    for s in Corpus.from_env().cli_syllabi():
        try:
            with database.transaction():
                Document.create(path=s.relative_path)
        except: pass


@cli.command()
def pull_overview_ids():

    """
    Copy document ids from Overview.
    """

    id = os.environ['OSP_DOC_SET_ID']
    ov = Overview.from_env()

    # Query for documents.
    docs = ov.list_documents(id).json()['items']

    for o_doc in docs:

        query = (
            Document
            .update(stored_id=o_doc['id'])
            .where(Document.path==o_doc['title'])
        )

        query.execute()


@cli.command()
def file_type_counts():

    """
    Print a list of file type -> count.
    """

    click.echo('Reading mime types...')

    # Count up the file types.
    counts = Counter()
    for s in Corpus.from_env().cli_syllabi():
        counts[s.libmagic_file_type] += 1

    # Print an ASCII table.
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
