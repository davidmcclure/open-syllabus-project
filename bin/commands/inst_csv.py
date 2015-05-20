

import click
import csv

from osp.institutions.models.institution import Institution
from osp.locations.models.doc_inst import Document_Institution
from osp.citations.hlom.models.citation import HLOM_Citation
from peewee import fn


@click.group()
def cli():
    pass


@cli.command()
@click.argument('out_file', type=click.File('w'))
def lonlats(out_file):

    """
    CSV with institution name and lon/lat, for Fusion Tables.
    """

    # CSV writer.
    cols = ['name', 'longitude', 'latitude']
    writer = csv.DictWriter(out_file, cols)
    writer.writeheader()

    # Select rows with coordinates.
    geocoded = (
        Institution
        .select()
        .where(Institution.metadata.contains('Latitude'))
    )

    for inst in geocoded:

        writer.writerow({
            'name': inst.metadata['Institution_Name'],
            'longitude': inst.metadata['Longitude'],
            'latitude': inst.metadata['Latitude']
        })


@cli.command()
@click.argument('out_file', type=click.File('w'))
def cited(out_file):

    """
    CSV with institution id, name, and citation count.
    """

    # CSV writer.
    cols = ['id', 'count', 'name']
    writer = csv.DictWriter(out_file, cols)
    writer.writeheader()

    count = fn.Count(HLOM_Citation.id)

    cited = (

        Institution
        .select(Institution, count)
        .join(Document_Institution)

        # Join citations.
        .join(HLOM_Citation, on=(
            Document_Institution.document==HLOM_Citation.document
        ))

        .group_by(Institution.id)
        .order_by(count.desc())

    )

    for inst in cited.naive():

        writer.writerow({
            'count': inst.count,
            'id': inst.id,
            'name': inst.metadata['Institution_Name'],
        })
