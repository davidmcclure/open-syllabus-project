

import click
import sys
import csv

from osp.common.models.base import pg_local, pg_remote, redis
from osp.citations.hlom.models.record import HLOM_Record
from osp.citations.hlom.models.citation import HLOM_Citation
from osp.citations.hlom.dataset import Dataset
from osp.citations.hlom.jobs.query import query
from osp.citations.hlom import queries
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
    pg_remote.connect()

    pg_local.create_tables([
        HLOM_Record
    ], safe=True)

    pg_remote.create_tables([
        HLOM_Citation
    ], safe=True)


@cli.command()
@click.option('--n', default=10000)
def insert_records(n):

    """
    Write the records into the database.
    """

    dataset = Dataset.from_env()

    i = 0
    for group in dataset.grouped_records(n):

        rows = []
        for record in group:

            # Just records with title/author.
            if record and record.title() and record.author():
                rows.append({
                    'control_number': record['001'].format_field(),
                    'record': record.as_marc()
                })

        if rows:
            HLOM_Record.insert_many(rows).execute()

        i += 1
        sys.stdout.write('\r'+str(i*n))
        sys.stdout.flush()


@cli.command()
def queue_queries():

    """
    Queue citation extraction queries.
    """

    queue = Queue(connection=redis)

    for record in HLOM_Record.select().naive().iterator():
        queue.enqueue(query, record.id)


@cli.command()
@click.argument('out_path', type=click.Path())
def csv_text_counts(out_path):

    """
    Write a CSV with text -> assignment count.
    """

    out_file = open(out_path, 'w')

    # CSV writer.
    cols = ['title', 'author', 'count', 'subjects']
    writer = csv.DictWriter(out_file, cols)

    rows = []
    for c in queries.text_counts().naive().iterator():

        row = HLOM_Record.get(
            HLOM_Record.control_number==c.record
        )

        # Gather subject field values.
        subjects = [s.format_field() for s in row.pymarc.subjects()]

        rows.append({
            'title': row.pymarc.title(),
            'author': row.pymarc.author(),
            'count': c.count,
            'subjects': ','.join(subjects)
        })

    writer.writeheader()
    writer.writerows(rows)


@cli.command()
@click.argument('out_path', type=click.Path())
def csv_syllabus_counts(out_path):

    """
    Write a CSV with syllabus -> citation count.
    """

    out_file = open(out_path, 'w')

    # CSV writer.
    cols = ['document', 'count']
    writer = csv.DictWriter(out_file, cols)

    rows = []
    for c in queries.syllabus_counts().naive().iterator():

        rows.append({
            'document': c.document,
            'count': c.count
        })

    writer.writeheader()
    writer.writerows(rows)


@cli.command()
@click.option('--page_len', default=50)
def write_objects(page_len):

    """
    Write HLOM records as store objects into Overview.
    """

    pass


@cli.command()
def pull_overview_ids():

    """
    Copy store object ids from Overview.
    """

    pass
