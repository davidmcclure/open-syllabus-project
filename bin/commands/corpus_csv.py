

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
@click.argument('in_file', type=click.File('r'))
@click.argument('out_file', type=click.File('w'))
@click.option('--r', default=250)
@click.option('--threshold', default=0.43)
def syllabus_refinement(in_file, out_file, r, threshold):

    """
    Select the N documents around a given threshold in the
    syllabus/not-syllabus classifier predictions.
    """

    cols = ['path', 'score']
    reader = csv.DictReader(in_file, cols)

    # Gather ordered (path, score) tuples.
    scores = [(r['path'], float(r['score'])) for r in reader]
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    # Get the index of the document at the threshold.
    center = min(
        range(len(scores)),
        key=lambda x: abs(scores[x][1]-threshold)
    )

    # CSV writer.
    cols = ['id', 'title', 'text']
    writer = csv.DictWriter(out_file, cols)
    writer.writeheader()

    for path, score in scores[center-r:center+r]:

        row = (
            Document_Text
            .select(Document_Text.text, Document.path)
            .join(Document)
            .where(Document.path==path)
            .naive()
            .first()
        )

        writer.writerow({
            'id': row.path,
            'title': row.path,
            'text': row.text
        })
