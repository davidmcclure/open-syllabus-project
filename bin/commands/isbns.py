

import click
import pickle
import csv

from osp.citations.hlom_corpus import HLOM_Corpus
from osp.citations.hlom_record import HLOM_Record
from osp.citations.models import Text_Index


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

        try:

            record = HLOM_Record(marc)

            isbn = marc.isbn()

            if isbn:
                isbns[record.control_number] = isbn

        except Exception as e:
            print(e)

        if i%1000 == 0:
            print(i)

    pickle.dump(isbns, out_file)


@cli.command()
@click.argument('in_file', type=click.File('rb'))
@click.argument('out_file', type=click.File('w'))
def isbn_to_text(in_file, out_file):

    """
    Link ISBNs -> text rankings.
    """

    isbns = pickle.load(in_file)

    cols = ['isbn', 'title', 'author', 'count']
    writer = csv.DictWriter(out_file, cols)
    writer.writeheader()

    for text in Text_Index.rank_texts():

        isbn = isbns.get(text['text'].identifier)

        writer.writerow(dict(
            isbn    = isbn,
            title   = text['text'].title,
            author  = text['text'].authors[0],
            count   = text['text'].count,
        ))
