

import click
import csv
import random

from osp.common.utils import query_bar
from osp.corpus.models.document import Document
from osp.corpus.models.text import Document_Text
from peewee import fn


@click.group()
def cli():
    pass


@cli.command()
@click.argument('out_path', type=click.Path())
@click.option('--frag_len', default=1500)
def truncated(out_path, frag_len):

    """
    Write a CSV with truncated document texts.
    """

    out_file = open(out_path, 'w')

    # CSV writer.
    cols = ['id', 'title', 'text']
    writer = csv.DictWriter(out_file, cols)
    writer.writeheader()

    query = (
        Document_Text
        .select(Document_Text.text, Document.path)
        .join(Document)
    )

    for row in query_bar(query):

        # Truncate the text.
        fragment = row.text[:frag_len]

        writer.writerow({
            'id': row.path,
            'title': row.path,
            'text': fragment
        })


@cli.command()
@click.argument('out_path', type=click.Path())
@click.option('--n', default=10000)
def random(out_path, n):

    """
    Write a CSV with truncated document texts.
    """

    out_file = open(out_path, 'w')

    # CSV writer.
    cols = ['id', 'title', 'text']
    writer = csv.DictWriter(out_file, cols)
    writer.writeheader()

    query = (
        Document_Text
        .select(Document_Text.text, Document.path)
        .join(Document)
        .order_by(fn.random())
        .limit(n)
    )

    for row in query_bar(query):

        writer.writerow({
            'id': row.path,
            'title': row.path,
            'text': row.text
        })
