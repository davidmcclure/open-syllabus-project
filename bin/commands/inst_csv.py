

import click
import csv

from peewee import fn

from osp.common.utils import read_csv
from osp.institutions.models import Institution, Institution_Document


@click.group()
def cli():
    pass


@cli.command()
@click.argument('out_file', type=click.File('w'))
@click.option('--n', default=1000)
def doc_to_inst(out_file, n):

    """
    Dump N institution -> document matches.
    """

    # CSV writer.
    cols = ['inst_url', 'doc_url']
    writer = csv.DictWriter(out_file, cols)
    writer.writeheader()

    # Pull matches.
    matches = Institution_Document.select().limit(n)

    for row in matches:

        writer.writerow(dict(
            inst_url=row.institution.url,
            doc_url=row.document.syllabus.url,
        ))


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
