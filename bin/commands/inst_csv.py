

import click
import csv

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
