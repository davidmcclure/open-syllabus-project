

import click

from osp.corpus.models import Document
from osp.common.utils import query_bar
from osp.institutions.models import Institution
from osp.institutions.models import Institution_Document
from osp.institutions.jobs import doc_to_inst

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


@cli.command()
def run_doc_to_inst():

    """
    Match documents -> institutions.
    """

    for doc in query_bar(Document.select()):
        try: doc_to_inst(doc.id)
        except: pass
