

import click

from osp.common.utils import query_bar
from osp.institutions.models import Institution, Institution_Document
from osp.corpus.models import Document

from peewee import create_model_tables


@click.group()
def cli():
    pass


@cli.command()
def init_db():

    """
    Create the database tables.
    """

    create_model_tables([
        Institution,
        Institution_Document,
    ], fail_silently=True)


@cli.command()
def ingest():

    """
    Ingest institutions.
    """

    Institution.ingest_usa()
    Institution.ingest_world()
