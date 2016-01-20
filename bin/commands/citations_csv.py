

import click
import csv

from osp.citations.models import Text, Citation
from osp.common.utils import query_bar

from peewee import fn


@click.group()
def cli():
    pass


@cli.command()
@click.argument('out_file', type=click.File('w'))
def fuzz(out_file):

    """
    Write a CSV with title and fuzz.
    """

    cols = [
        'count',
        'fuzz',
        'surname',
        'title',
    ]

    writer = csv.DictWriter(out_file, cols)
    writer.writeheader()

    count = fn.count(Citation.id)

    query = (
        Text
        .select(Text, count)
        .join(Citation)
        .where(Text.display==True)
        .having(count > 100)
        .group_by(Text.id)
        .naive()
    )

    for t in query_bar(query):

        writer.writerow(dict(
            count=t.count,
            fuzz=t.fuzz,
            surname=t.surname,
            title=t.title,
        ))
