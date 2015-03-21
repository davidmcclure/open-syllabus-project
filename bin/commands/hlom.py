

import click
import numpy as np
import csv

from osp.common.config import config
from osp.citations.hlom.models.record import HLOM_Record
from osp.citations.hlom.models.citation import HLOM_Citation
from osp.citations.hlom.dataset import Dataset
from osp.citations.hlom.jobs.query import query
from osp.citations.hlom import queries
from peewee import create_model_tables
from playhouse.postgres_ext import ServerSide


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
        HLOM_Citation,
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
@click.argument('out_path', type=click.Path())
def csv_text_counts(out_path):

    """
    Write a CSV with text -> assignment count.
    """

    out_file = open(out_path, 'w')

    # CSV writer.
    cols = ['title', 'author', 'count', 'subjects']
    writer = csv.DictWriter(out_file, cols)
    writer.writeheader()

    rows = []
    for c in queries.text_counts().naive().iterator():

        row = HLOM_Record.get(
            HLOM_Record.control_number==c.record
        )

        # Gather subject field values.
        subjects = [s.format_field() for s in row.pymarc.subjects()]

        rows.append({
            'title': row.pymarc.title(),
            'author': row.pymarc.author(),
            'count': c.count,
            'subjects': ','.join(subjects)
        })

    writer.writerows(rows)


@cli.command()
@click.argument('out_path', type=click.Path())
def csv_syllabus_counts(out_path):

    """
    Write a CSV with syllabus -> citation count.
    """

    out_file = open(out_path, 'w')

    # CSV writer.
    cols = ['document', 'count']
    writer = csv.DictWriter(out_file, cols)
    writer.writeheader()

    rows = []
    for c in queries.syllabus_counts().naive().iterator():

        rows.append({
            'document': c.document,
            'count': c.count
        })

    writer.writerows(rows)
