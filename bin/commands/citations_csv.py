

import click
import csv

from osp.common.utils import query_bar
from osp.citations.models import Citation


@click.group()
def cli():
    pass


@cli.command()
@click.argument('out_file', type=click.File('w'))
@click.option('--n', default=100000)
def fuzz(out_file, n):

    """
    Write N citation fuzz scores.
    """

    cols = ['fuzz', 'tokens']
    writer = csv.DictWriter(out_file, cols)
    writer.writeheader()

    query = (
        Citation.select()
        .order_by(Citation.id)
        .limit(n)
    )

    for c in query_bar(query):

        writer.writerow(dict(
            fuzz = c.fuzz,
            tokens = c.tokens,
        ))
