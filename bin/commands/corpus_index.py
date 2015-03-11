

import click
import math

from osp.common.utils import query_bar
from osp.common.models.base import redis, elasticsearch as es
from osp.corpus.queries import all_document_texts
from elasticsearch.helpers import bulk
from blessings import Terminal
from rq import Queue


@click.group()
def cli():
    pass


@cli.command()
def create():

    """
    Create the index.
    """

    es.indices.create('osp', {
        'mappings': {
            'syllabus': {
                '_id': {
                    'index': 'not_analyzed',
                    'store': True
                },
                'properties': {
                    'body': {
                        'type': 'string'
                    }
                }
            }
        }
    })


@cli.command()
def delete():

    """
    Delete the index.
    """

    es.indices.delete('osp')


@cli.command()
def count():

    """
    Count documents.
    """

    click.echo(es.count('osp', 'syllabus')['count'])


@cli.command()
def insert():

    """
    Index documents.
    """

    query = query_bar(all_document_texts())

    def stream():
        for row in query:
            yield {'_id': row.id, 'body': row.text}

    # Batch-insert the documents.
    bulk(es, stream(), index='osp', doc_type='syllabus')


@cli.command()
@click.argument('q')
@click.option('--size', default=10)
@click.option('--start', default=0)
@click.option('--slop', default=10)
def search(q, size, start, slop):

    """
    Search documents.
    """

    results = es.search('osp', 'syllabus', timeout=30, body={
        'size': size,
        'from': start,
        'fields': [],
        'query': {
            'match_phrase': {
                'body': {
                    'query': q,
                    'slop': slop
                }
            }
        },
        'highlight': {
            'pre_tags': ['\033[1m'],
            'post_tags': ['\033[0m'],
            'fields': {
                'body': {}
            }
        }
    })

    term = Terminal()

    # Total hits.
    hits = str(results['hits']['total'])+' docs'
    click.echo(term.standout_cyan(hits))

    # Hit highlights.
    for hit in results['hits']['hits']:
        click.echo('\n'+term.underline(hit['_id']))
        for hl in hit['highlight']['body']:
            click.echo(hl)
