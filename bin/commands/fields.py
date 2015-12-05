

import click

from osp.common.config import config
from osp.corpus.models.document_text import Document_Text
from osp.fields.models.field import Field
from osp.fields.models.field_document import Field_Document
from osp.fields.jobs.ext_fields import ext_fields

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
        Field_Document,
    ], fail_silently=True)


@cli.command()
def insert_fields():

    """
    Insert field rows.
    """

    Field.insert_fields()


@cli.command()
@click.option('--n', default=10000)
def queue_queries(n):

    """
    Queue query tasks in the worker.
    """

    for text in Document_Text.select().limit(n):
        config.rq.enqueue(ext_fields, text.document_id)
