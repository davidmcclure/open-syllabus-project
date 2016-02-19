

import os
import click
import json

from osp.www import utils
from osp.www.hit import Hit

from clint.textui import progress
from slugify import slugify


@click.group()
def cli():
    pass


@cli.command()
@click.argument('path', type=click.Path())
@click.option('--size', default=10000)
def dump(path, size):

    """
    Write overall rankings.
    """

    dump_overall(
        os.path.join(path, 'overall.json'),
        size,
    )

    dump_facets(
        utils.field_facets(),
        'field_id',
        os.path.join(path, 'fields'),
        size,
    )

    dump_facets(
        utils.institution_facets(),
        'institution_id',
        os.path.join(path, 'institutions'),
        size,
    )

    dump_facets(
        utils.state_facets(),
        'state',
        os.path.join(path, 'states'),
        size,
    )


def dump_overall(path, size):

    """
    Write overall rankings.
    """

    overall = utils.rank_texts.uncached(size=size)
    dump_ranks(overall, path)


def dump_facets(facets, key, path, size):

    """
    Write overall rankings.
    """

    for f in progress.bar(facets):

        ranks = utils.rank_texts.uncached(
            filters={ key: f['value'] },
            size=size,
        )

        fname = '{0}.json'.format(slugify(f['label']))
        fpath = os.path.join(path, fname)

        dump_ranks(ranks, fpath)


def dump_ranks(ranks, path):

    """
    Write ranks to a file.
    """

    dirname = os.path.dirname(path)

    if not os.path.exists(dirname):
        os.makedirs(dirname)

    rows = []
    for t in ranks['hits']:
        rows.append(Hit(t).csv_row)

    with open(path, 'w') as fh:
        json.dump(rows, fh, indent=2)
