

import click
import json

from osp.www import utils
from osp.www.hit import Hit


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

    ranks = utils.rank_texts.uncached(size=n)
    dump_ranks(ranks, out_file)


def dump_ranks(ranks, fh):

    """
    Write ranks to a file.
    """

    rows = []
    for t in ranks['hits']:
        rows.append(Hit(t).csv_row)

    json.dump(rows, fh, indent=2)
