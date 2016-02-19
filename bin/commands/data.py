

import click
import json

from osp.www.utils import rank_texts


@click.group()
def cli():
    pass


@cli.command()
@click.argument('out_file', type=click.File('w'))
@click.option('--n', default=10000)
def overall(out_file, n):

    """
    Write overall rankings.
    """

    ranks = rank_texts.uncached(size=n)
    json.dump(ranks, out_file, indent=2)
