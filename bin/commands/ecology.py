

import click
import pickle

from osp.corpus.models import Document
from osp.common import config


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


@cli.command()
@click.argument('query', type=str)
@click.argument('in_file', type=click.File('rb'))
def query_urls(query, in_file):

    """
    Query docs for a keyword, join URLs, write to CSV.
    """

    print(query)
