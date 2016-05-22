

import click

from osp.common import config
from osp.models import BaseModel


@click.group()
def cli():
    pass


@cli.command()
def create_tables():

    """
    Create the database tables.
    """

    engine = config.build_engine()

    BaseModel.metadata.create_all(engine)
