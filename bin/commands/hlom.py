

import click
import sys
import csv

from osp.common.models.base import pg_worker, pg_server, redis
from osp.citations.hlom.models.record import HLOM_Record
from osp.citations.hlom.models.citation import HLOM_Citation
from osp.citations.hlom.dataset import Dataset
from osp.citations.hlom.jobs.query import query
from osp.citations.hlom import queries
from pymarc.record import Record
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

    pg_worker.connect()
    pg_server.connect()

    pg_worker.create_tables([
        HLOM_Record
    ], safe=True)

    pg_server.create_tables([
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
        queue.enqueue(query, record.control_number)


@cli.command()
@click.argument('out_path', type=click.Path())
def write_csv(out_path):

    """
    Write a CSV with title/author -> count.
    """

    out_file = open(out_path, 'w')

    # CSV writer.
    cols = ['title', 'author', 'count']
    writer = csv.DictWriter(out_file, cols)

    rows = []
    for c in queries.text_counts().naive().iterator():

        marc = HLOM_Record.get(
            HLOM_Record.control_number==c.record
        )

        # Hydrate a MARC record.
        record = Record(data=bytes(marc.record))

        rows.append({
            'title': record.title(),
            'author': record.author(),
            'count': c.count
        })

    writer.writeheader()
    writer.writerows(rows)
