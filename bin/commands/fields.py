

import click

from osp.fields.models.field import Field
from osp.fields.models.field_document import Field_Document
from osp.fields.jobs.query import query
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
def queue_queries():

    """
    Queue query tasks in the worker.
    """

    for field in Field.select():
        config.rq.enqueue(query, field.id)
