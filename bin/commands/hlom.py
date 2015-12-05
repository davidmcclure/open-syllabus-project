

import click
import numpy as np
import csv

from osp.common.config import config
from osp.hlom.models.record import HLOM_Record
from osp.hlom.models.record_cited import HLOM_Record_Cited
from osp.hlom.models.citation import HLOM_Citation
from osp.hlom.models.node import HLOM_Node
from osp.hlom.models.edge import HLOM_Edge
from osp.hlom.dataset import Dataset
from osp.hlom.jobs.hlom_to_docs import hlom_to_docs
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
        HLOM_Record,
        HLOM_Record_Cited,
        HLOM_Citation,
        HLOM_Node,
        HLOM_Edge,
    ], fail_silently=True)


@cli.command()
@click.option('--page_size', default=10000)
def insert_records(page_size):

    """
    Write the records into the database.
    """

    HLOM_Record.insert_records(page_size)


@cli.command()
def queue_queries():

    """
    Queue citation extraction queries.
    """

    for record in ServerSide(HLOM_Record.select()):
        config.rq.enqueue(hlom_to_docs, record.id)
