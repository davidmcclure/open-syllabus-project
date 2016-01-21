

import click
import csv

from osp.citations.models import Text, Citation, Text_Index

from peewee import fn


@click.group()
def cli():
    pass


@cli.command()
@click.argument('out_file', type=click.File('w'))
@click.option('--min_count', default=100)
def fuzz(out_file, min_count):

    """
    Write a CSV with title and fuzz.
    """

    cols = [
        'text_id',
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
        .having(count > min_count)
        .group_by(Text.id)
        .naive()
    )

    texts = list(query)

    # Sort on fuzz, high -> low.
    for t in sorted(texts, key=lambda t: t.fuzz, reverse=True):

        writer.writerow(dict(
            text_id=t.id,
            count=t.count,
            fuzz=t.fuzz,
            surname=t.surname,
            title=t.title,
        ))


@cli.command()
@click.argument('out_file', type=click.File('w'))
@click.option('--depth', default=1000)
def fuzz(out_file, depth):

    """
    Write the top N text ranks.
    """

    cols = [
        'count',
        'title',
        'author',
    ]

    writer = csv.DictWriter(out_file, cols)
    writer.writeheader()

    ranks = Text_Index.rank_texts()
    ranks = sorted(ranks, key=lambda x: x['rank'])

    for r in ranks:

        text = r['text']

        writer.writerow(dict(
            count=text.count,
            title=text.title,
            author=text.authors[0],
        ))
