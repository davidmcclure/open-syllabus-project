

import click
import csv
import random

from osp.common.utils import query_bar
from osp.corpus.models.text import Document_Text


@click.group()
def cli():
    pass


@cli.command()
@click.argument('out_path', type=click.Path())
@click.option('--frag_len', default=1500)
@click.option('--page_len', default=10000)
def truncated(out_path, frag_len, page_len):

    """
    Write a CSV with truncated document texts.
    """

    out_file = open(out_path, 'w')

    # CSV writer.
    cols = ['id', 'title', 'text']
    writer = csv.DictWriter(out_file, cols)
    writer.writeheader()

    for row in query_bar(Document_Text.select()):

        # Truncate the text.
        fragment = row.text[:frag_len]

        writer.writerow({
            'id': row.document,
            'title': row.document,
            'text': fragment
        })
