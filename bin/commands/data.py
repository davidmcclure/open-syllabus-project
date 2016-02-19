

import os
import click
import json

from osp.www import utils
from osp.www.hit import Hit

from slugify import slugify


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


@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--n', default=10000)
def fields(path, n):

    """
    Write overall rankings.
    """

    dump_facets(utils.field_facets(), 'field_id', path, n)


def dump_facets(facets, key, path, n):

    """
    Write overall rankings.
    """

    fields = utils.field_facets()

    for f in facets:

        ranks = utils.rank_texts.uncached(
            filters={ key: f['value'] },
            size=n,
        )

        fname = '{0}.json'.format(slugify(f['label']))
        fpath = os.path.join(path, fname)

        with open(fpath, 'w') as fh:
            dump_ranks(ranks, fh)


def dump_ranks(ranks, fh):

    """
    Write ranks to a file.
    """

    rows = []
    for t in ranks['hits']:
        rows.append(Hit(t).csv_row)

    json.dump(rows, fh, indent=2)
