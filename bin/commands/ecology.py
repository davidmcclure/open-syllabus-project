

import click
import pickle

from osp.corpus.models import Document


@click.group()
def cli():
    pass


@cli.command()
@click.argument('out_file', type=click.File('wb'))
def doc_to_url(out_file):

    """
    Map document id -> URL.
    """

    urls = {}
    for doc in Document.select():
        urls[doc.id] = doc.syllabus.url

    pickle.dump(urls, out_file)
