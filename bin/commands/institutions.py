

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
def queue_geocoding():

    """
    Queue geocoding tasks in the worker.

    :param in_file: A handle on the input CSV.
    """

    queue = Queue(connection=redis)

    for inst in Institution.select().iterator():
        query = inst.geocoding_query
        if query: queue.enqueue(geocode, inst.id, query)


@cli.command()
@click.argument('out_path', type=click.Path())
def write_csv(out_path):

    """
    Generate a CSV file.
    """

    out_file = open(out_path, 'w')

    # CSV writer.
    cols = ['name', 'longitude', 'latitude']
    writer = csv.DictWriter(out_file, cols)
    writer.writeheader()

    rows = []
    for inst in queries.csv_rows().naive().iterator():
        rows.append({
            'name': inst.metadata['Institution_Name'],
            'latitude': inst.lat,
            'longitude': inst.lon
        })

    writer.writerows(rows)
