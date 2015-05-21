

import click
import numpy as np
import csv

from osp.common.config import config
from osp.citations.hlom.models.record import HLOM_Record
from osp.citations.hlom.models.record_cited import HLOM_Record_Cited
from osp.citations.hlom.models.citation import HLOM_Citation
from osp.citations.hlom.models.node import HLOM_Node
from osp.citations.hlom.models.edge import HLOM_Edge
from osp.citations.hlom.dataset import Dataset
from osp.citations.hlom.jobs.query import query
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
        config.rq.enqueue(query, record.id)


@cli.command()
@click.argument('out_file', type=click.File('w'))
def csv_text_counts(out_file):

    """
    Write a CSV with text -> assignment count.
    """

    # CSV writer.
    cols = ['id', 'title', 'author', 'count']
    writer = csv.DictWriter(out_file, cols)
    writer.writeheader()

    query = HLOM_Citation.text_counts()
    count = query.count()

    rows = []
    for c in bar(query.naive().iterator(),
                 expected_size=count):

        writer.writerow({
            'id':       c.record.id,
            'title':    c.record.marc.title(),
            'author':   c.record.marc.author(),
            'count':    c.count
        })


# TODO|dev


@cli.command()
def write_stats():

    """
    Cache citation counts / deduping hashes.
    """

    HLOM_Record.write_stats()


@cli.command()
def write_metrics():

    """
    Cache teaching ranks / percentiles.
    """

    HLOM_Record.write_metrics()
