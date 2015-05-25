

import click
import csv

from osp.common.utils import query_bar
from osp.citations.hlom.models.record import HLOM_Record
from osp.citations.hlom.models.citation import HLOM_Citation
from osp.citations.hlom.counts import Counts
from osp.corpus.utils import tokenize


@click.group()
def cli():
    pass


@cli.command()
@click.argument('out_file', type=click.File('w'))
@click.option('--min_rank', default=2000)
def common(out_file, min_rank):

    """
    Texts that get excluded by the word-frequency filter.
    """

    # CSV writer.
    cols = ['title', 'author']
    writer = csv.DictWriter(out_file, cols)
    writer.writeheader()

    counts = Counts()

    for r in query_bar(HLOM_Record.select_unique()):

        t = [t['stemmed'] for t in tokenize(r.marc.title())]
        a = [t['stemmed'] for t in tokenize(r.marc.author())]

        ranks = []
        for token in set.union(set(t), set(a)):
            rank = counts.rank(token)
            if rank:
                ranks.append(rank)

        # No infrequent terms.
        if max(ranks) < min_rank:
            writer.writerow({
                'title': r.marc.title(),
                'author': r.marc.author(),
            })
