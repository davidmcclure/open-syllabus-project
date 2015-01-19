

import click

from osp.common.models.base import postgres, redis
from osp.citations.hlbd.models.record import HLBD_Record
from osp.citations.hlbd.dataset import Dataset


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
        HLBD_Record
    ], safe=True)


@cli.command()
@click.option('--n', default=1000)
def insert_records(n):

    """
    Write the records into the database.
    """

    dataset = Dataset.from_env()

    # TODO|dev
    for group in dataset.grouped_records(n):
        print(group)
