

import click
import csv

from osp.common.models.base import database
from osp.common.overview import Overview
from osp.institutions.models.institution import Institution
from osp.institutions.models.lonlat import LonLat
from osp.institutions.jobs.geocode import geocode
from rq import Queue
from redis import StrictRedis
from peewee import *


@click.group()
def cli():
    pass


@cli.command()
def init_db():

    """
    Create the database tables.
    """

    database.connect()
    database.create_tables([Institution, LonLat])


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

    with database.transaction():
        Institution.insert_many(rows).execute()


@cli.command()
def queue_geocoding():

    """
    Queue geocoding tasks in the worker.

    :param in_file: A handle on the input CSV.
    """

    # TODO: ENV-ify.
    queue = Queue(connection=StrictRedis())

    for inst in Institution.select().iterator():
        queue.enqueue(geocode, inst.id, inst.geocoding_query)


@cli.command()
@click.option('--page', default=50)
def write_objects(page):

    """
    Write store objects into Overview.
    """

    ov = Overview.from_env()

    # Join the coordinates.
    query = Institution.join_lonlats()

    objects = []
    for inst in query.naive().iterator():

        inst.metadata.update({
            'Longitude': inst.lon,
            'Latitude': inst.lat
        })

        objects.append({
            'indexedLong': inst.id,
            'indexedString': inst.metadata['Institution_Name'],
            'json': inst.metadata
        })

    # Write the objects in pages.
    for i in range(0, len(objects), page):
        ov.post_object(objects[i:i+page])


@cli.command()
def pull_overview_ids():

    """
    Copy document ids from Overview.
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
def make_csv(out_path):

    """
    Generate a CSV file.

    :param in_file: A path for the new CSV file.
    """

    out_file = open(out_path, 'w')
    cols = ['name', 'lon', 'lat']

    # CSV writer:
    writer = csv.DictWriter(out_file, cols)

    # Join the coordinates.
    query = Institution.join_lonlats()

    rows = []
    for inst in query.naive().iterator():
        rows.append({
            'name': inst.metadata['Institution_Name'],
            'lon': inst.lon,
            'lat': inst.lat
        })

    writer.writeheader()
    writer.writerows(rows)


@cli.command()
def institution_count():

    """
    How many institutions are registered locally?
    """

    click.echo(Institution.select().count())


@cli.command()
def object_count():

    """
    How many institutions are loaded into Overview?
    """

    ov = Overview.from_env()
    click.echo(len(ov.list_objects().json()))
