

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
@click.argument('out_file', type=click.File('w'))
@click.option('--frag_len', default=1500)
def truncated(out_file, frag_len):

    """
    Write a CSV with truncated document texts.
    """

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
@click.argument('out_file', type=click.File('w'))
@click.option('--n', default=10000)
def random(out_file, n):

    """
    Write a CSV with plaintext for N random docs.
    """

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


@cli.command()
@click.argument('out_file', type=click.File('w'))
@click.option('--n', default=10000)
@click.option('--threshold', default=0.43)
def syllabus_refinement(out_path, n, threshold):

    """
    Select the N documents around a given threshold in the
    syllabus/not-syllabus classifier predictions.
    """

    pass
