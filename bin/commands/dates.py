

import click

from osp.common.models.base import postgres, redis
from osp.dates.models.date import Date


@click.group()
def cli():
    pass


@cli.command()
def init_db():

    """
    Create the database tables.
    """

    postgres.connect()
    postgres.create_tables([Date], safe=True)
