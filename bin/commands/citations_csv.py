

import click
import csv

from osp.common.utils import query_bar
from osp.corpus.citations import Citation


@click.group()
def cli():
    pass


@cli.command()
@click.argument('out_file', type=click.File('w'))
@click.option('--n', default=None)
def min_freqs(out_file, n):

    """
    Write min-frequency scores for N citations.
    """

    cols = ['min_freq', 'tokens']
    writer = csv.DictWriter(out_file, cols)
    writer.writeheader()

    for c in query_bar(Citation.select().limit(n)):

        writer.writerow(dict(
            min_freq = c.min_freq,
            tokens = c.tokens,
        ))
