

import click
import csv

from osp.common.utils import query_bar
from osp.citations.models import Text


@click.group()
def cli():
    pass


@cli.command()
@click.argument('out_file', type=click.File('w'))
def fuzz(out_file):

    """
    Write a CSV with title and fuzz.
    """

    cols = ['fuzz', 'title']
    writer = csv.DictWriter(out_file, cols)
    writer.writeheader()

    query = (
        Text.select()
        .where(Text.display==True)
        .where(Text.valid==True)
    )

    for t in query_bar(query):
        writer.writerow(dict(fuzz=t.fuzz, title=t.title))
