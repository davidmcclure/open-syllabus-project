

import click
import pickle

from osp.citations.hlom_corpus import HLOM_Corpus
from osp.citations.hlom_record import HLOM_Record


@click.group()
def cli():
    pass


@cli.command()
@click.argument('out_file', type=click.File('wb'))
def control_to_isbn(out_file):

    """
    Map control numbers -> ISBNs.
    """

    corpus = HLOM_Corpus.from_env()

    isbns = {}
    for i, marc in enumerate(corpus.records()):

        record = HLOM_Record(marc)

        isbn = marc.isbn()

        if isbn:
            isbns[record.control_number] = isbn

        if i%1000 == 0:
            print(i)

    pickle.dump(isbns, out_file)
