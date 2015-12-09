

import click
import numpy as np
import csv

from osp.common.config import config
from osp.citations.models import Text
from osp.citations.models import HLOM_Citation
from osp.citations.hlom_corpus import HLOM_Corpus
from osp.citations.jobs import hlom_to_docs
from peewee import create_model_tables
from playhouse.postgres_ext import ServerSide
from clint.textui.progress import bar


@click.group()
def cli():
    pass


@cli.command()
def init_db():

    """
    Create the database tables.
    """

    create_model_tables([
        Text,
        HLOM_Citation,
    ], fail_silently=True)


@cli.command()
@click.option('--page_size', default=10000)
def insert_records(page_size):

    """
    Write the records into the database.
    """

    Text.insert_records(page_size)


@cli.command()
def queue_queries():

    """
    Queue citation extraction queries.
    """

    for record in ServerSide(Text.select()):
        config.rq.enqueue(hlom_to_docs, record.id)
