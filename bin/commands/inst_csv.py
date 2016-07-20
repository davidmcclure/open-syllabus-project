

import click
import csv

from osp.common.utils import query_bar, read_csv
from osp.institutions.models import Institution, Institution_Document
from peewee import fn


@click.group()
def cli():
    pass


@cli.command()
@click.argument('out_file', type=click.File('w'))
def usa_doc_counts(out_file):

    """
    Update the institutions CSV with the number of docs in the OSP corpus.
    """

    reader = read_csv('osp.institutions', 'data/usa.csv')

    cols = reader.fieldnames + ['osp_doc_count']

    writer = csv.DictWriter(out_file, cols)
    writer.writeheader()

    for row in reader:

        count = fn.count(Institution_Document.id)

        query = (
            Institution_Document
            .select(count)
            .join(Institution)
            .where(Institution.url == row['web_url'])
        )

        row['osp_doc_count'] = query.scalar()

        writer.writerow(row)


@cli.command()
@click.argument('out_file', type=click.File('w'))
def world_doc_counts(out_file):

    """
    Update the institutions CSV with the number of docs in the OSP corpus.
    """

    reader = read_csv('osp.institutions', 'data/world.csv')

    cols = reader.fieldnames + ['osp_doc_count']

    writer = csv.DictWriter(out_file, cols)
    writer.writeheader()

    for row in reader:

        count = fn.count(Institution_Document.id)

        query = (
            Institution_Document
            .select(count)
            .join(Institution)
            .where(Institution.url == row['url'])
        )

        row['osp_doc_count'] = query.scalar()

        writer.writerow(row)
