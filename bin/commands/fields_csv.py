

import csv
import click

from osp.fields.models import Field
from osp.fields.models import Field_Document
from osp.common.utils import query_bar


@click.group()
def cli():
    pass


@cli.command()
@click.argument('out_file', type=click.File('w'))
@click.option('--n', default=10000)
def matches(out_file, n):

    """
    Write a CSV with field name -> snippet.
    """

    # CSV writer.
    cols = ['name', 'snippet']
    writer = csv.DictWriter(out_file, cols)
    writer.writeheader()

    query = (
        Field_Document
        .select(Field_Document.snippet, Field.secondary_field)
        .join(Field)
        .limit(n)
    )

    for row in query_bar(query):

        writer.writerow({
            'name': row.secondary_field,
            'snippet': row.snippet,
        })
