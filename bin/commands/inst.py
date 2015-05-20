

import click
import csv

from osp.common.config import config
from osp.institutions.models.institution import Institution
from osp.institutions.jobs.geocode import geocode
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
    ], fail_silently=True)


@cli.command()
def insert_institutions():

    """
    Insert institution rows.
    """

    Institution.insert_institutions()


@cli.command()
def queue_geocode():

    """
    Queue geocoding tasks in the worker.

    :param in_file: A handle on the input CSV.
    """

    for inst in Institution.select():
        config.rq.enqueue(geocode, inst.id)
