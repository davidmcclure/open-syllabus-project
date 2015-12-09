

import click

from osp.common.config import config
from osp.corpus.models import Document_Text
from osp.fields.models import Field
from osp.fields.models import Subfield
from osp.fields.models import Subfield_Document
from osp.fields.jobs import doc_to_fields

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
        Field,
        Subfield,
        Subfield_Document,
    ], fail_silently=True)


@cli.command()
def ingest():

    """
    Load fields.
    """

    Field.ingest()
    Subfield.ingest()
