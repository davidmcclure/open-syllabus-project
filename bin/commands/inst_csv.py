

import click
import csv

from peewee import fn

from osp.common.utils import read_csv
from osp.institutions.models import Institution
from osp.institutions.models import Institution_Document


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
def counts(out_file):

    """
    Update the institutions CSV with the number of docs in the OSP corpus.
    """

    cols = ['name', 'url', 'count']
    writer = csv.DictWriter(out_file, cols)
    writer.writeheader()

    count = fn.count(Institution_Document.id)

    query = (
        Institution
        .select(Institution, count)
        .join(Institution_Document)
        .group_by(Institution.id)
        .order_by(count.desc())
    )

    for row in query:

        writer.writerow(dict(
            name=row.name,
            url=row.url,
            count=row.count,
        ))
