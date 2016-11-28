

import click
import pickle
import csv

from osp.corpus.models import Document
from osp.common.utils import query_bar
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
    for doc in query_bar(Document.select()):
        urls[doc.id] = doc.syllabus.url()

    pickle.dump(urls, out_file)


@cli.command()
@click.argument('query')
@click.argument('urls_file', type=click.File('rb'))
@click.argument('csv_file', type=click.File('w'))
@click.option('--size', default=1000)
def query_urls(query, urls_file, csv_file, size):

    """
    Query docs for a keyword, join URLs, write to CSV.
    """

    urls = pickle.load(urls_file)

    # Query for docs.
    results = config.es.search(

        index='document',
        request_timeout=90,

        body={
            'fields': [],
            'size': size,
            'query': {
                'match': {
                    'body': query
                }
            },
            'highlight': {
                'pre_tags': ['***'],
                'post_tags': ['***'],
                'fields': {
                    'body': {
                        'number_of_fragments': 10,
                        'fragment_size': 100,
                    },
                }
            }
        },

    )

    writer = csv.DictWriter(csv_file, [
        'id',
        'score',
        'url',
        'snippets',
    ])

    writer.writeheader()

    if results['hits']['total'] > 0:
        for hit in results['hits']['hits']:

            url = urls.get(int(hit['_id']))

            # Strip newlines, join highlights.
            snippets = '\n------\n'.join([
                hl.replace('\n', ' ')
                for hl in hit['highlight']['body']
            ])

            writer.writerow(dict(
                id=hit['_id'],
                score=hit['_score'],
                url=url,
                snippets=snippets,
            ))
