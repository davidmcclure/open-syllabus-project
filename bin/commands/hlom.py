

import click

from osp.common.models.base import postgres, redis
from osp.citations.hlom.models.record import HLOM_Record
from osp.citations.hlom.jobs.query import query
from osp.citations.hlom.dataset import Dataset


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
        HLOM_Record
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
            if record.title() and record.author():
                rows.append({
                    'control_number': record['001'],
                    'record': record.as_marc()
                })

        HLOM_Record.insert_many(rows).execute()

        i += 1
        click.echo(i*n)


@cli.command()
def queue_queries():

    """
    Queue citation extraction queries.
    """

    dataset = Dataset.from_env()

    for record in HLOM_Record.select().naive().iterator():
        query(record.control_number)

        #q = record.title()
        #if q and record.author():
            #q += str(record.author())

        #click.echo(q)
