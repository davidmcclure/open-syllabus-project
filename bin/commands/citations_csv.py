

import click
import csv
import numpy as np

from osp.common.utils import query_bar
from osp.citations.models import Citation

from clint.textui import progress


@click.group()
def cli():
    pass


@cli.command()
@click.argument('out_file', type=click.File('w'))
@click.option('--n', default=100000)
def fuzz(out_file, n):

    """
    Write N citation fuzz scores.
    """

    cols = ['fuzz', 'tokens']
    writer = csv.DictWriter(out_file, cols)
    writer.writeheader()

    # Draw N random ids.
    cids = np.random.random_integers(1, Citation.max_id(), n)

    for cid in progress.bar(cids):

        try:

            c = Citation.get(Citation.id==cid)

            writer.writerow(dict(
                fuzz=c.fuzz,
                tokens=c.tokens,
            ))

        except:
            pass
