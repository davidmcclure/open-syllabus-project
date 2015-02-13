

import os
import click
import csv

from osp.common.config import config
from osp.common.models.base import pg_local, redis
from osp.common.overview import Overview
from osp.institutions.models.institution import Institution
from osp.institutions.models.lonlat import Institution_LonLat
from osp.institutions.jobs.geocode import geocode
from osp.institutions import queries
from rq import Queue
from peewee import *


@click.group()
def cli():
    pass


@cli.command()
def init_db():

    """
    Create the database tables.
    """

    pg_local.connect()

    pg_local.create_tables([
        Institution,
        Institution_LonLat
    ], safe=True)


@cli.command()
@click.argument('in_file', type=click.File('rt'))
def insert_institutions(in_file):

    """
    Write the institutions into the database.

    :param in_file: A handle on the input CSV.
    """

    if Institution.select().count():
        click.confirm('Already inserted. Continue?', abort=True)

    reader = csv.DictReader(in_file)

    rows = []
    for row in reader:
        rows.append({'metadata': row})

    with pg_local.transaction():
        Institution.insert_many(rows).execute()


@cli.command()
def queue_geocoding():

    """
    Queue geocoding tasks in the worker.

    :param in_file: A handle on the input CSV.
    """

    queue = Queue(connection=redis)

    for inst in Institution.select().iterator():
        query = inst.geocoding_query
        if query:queue.enqueue(geocode, inst.id, query)


@cli.command()
@click.option('--page', default=50)
def write_objects(page):

    """
    Write store objects into Overview.
    """

    ov = Overview.from_env()

    objects = []
    for inst in queries.store_objects().naive().iterator():

        json = { k: inst.metadata[k] for k in [
            'Institution_Name',
            'Campus_Name',
            'Institution_Web_Address'
        ]}

        json.update({
            'Longitude': inst.lon,
            'Latitude': inst.lat
        })

        objects.append({
            'indexedLong': inst.id,
            'indexedString': inst.metadata['Institution_Name'],
            'json': json
        })

    # Write the objects in pages.
    for i in range(0, len(objects), page):
        ov.post_object(objects[i:i+page])


@cli.command()
def pull_overview_ids():

    """
    Copy store object ids from Overview.
    """

    ov = Overview.from_env()

    for obj in ov.list_objects().json():

        query = (
            Institution
            .update(stored_id=obj['id'])
            .where(Institution.id==obj['indexedLong'])
        )

        query.execute()


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

    rows = []
    for inst in queries.csv_rows().naive().iterator():
        rows.append({
            'name': inst.metadata['Institution_Name'],
            'latitude': inst.lat,
            'longitude': inst.lon
        })

    writer.writeheader()
    writer.writerows(rows)
