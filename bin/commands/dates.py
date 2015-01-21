

import click

from osp.common.models.base import postgres, redis
from osp.dates.semester.models.semester import Document_Semester
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
        Document_Semester
    ], safe=True)
