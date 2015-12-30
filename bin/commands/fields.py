

import click

from osp.corpus.models import Document
from osp.common.utils import query_bar
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

    Subfield.ingest()


@cli.command()
def run_doc_to_fields():

    """
    Match documents -> fields.
    """

    for doc in query_bar(Document.select()):
        try: doc_to_fields(doc.id)
        except: pass
