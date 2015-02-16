

import math
import click
import re

from osp.common.models.base import redis, elasticsearch as es
from osp.citations.hlom.jobs.index import index
from osp.citations.hlom import queries
from pymarc import Record
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

    es.indices.create('hlom', {
        'mappings': {
            'record': {
                '_id': {
                    'index': 'not_analyzed',
                    'store': True
                },
                'properties': {
                    'title': {
                        'type': 'string'
                    },
                    'author': {
                        'type': 'string'
                    },
                    'publisher': {
                        'type': 'string'
                    },
                    'pubyear': {
                        'type': 'string'
                    },
                    'count': {
                        'type': 'integer'
                    },
                    'stored_id': {
                        'type': 'integer'
                    },
                    'lists': {
                        'properties': {
                            'subjects': {
                                'type': 'string'
                            },
                            'notes': {
                                'type': 'string'
                            }
                        }
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

    es.indices.delete('hlom')


@cli.command()
def count():

    """
    Count documents.
    """

    click.echo(es.count('hlom', 'record')['count'])


@cli.command()
@click.option('--n', default=10000)
def queue_insert(n):

    """
    Index documents.
    """

    queue = Queue(connection=redis)
    query = queries.records_with_citations()
    pages = math.ceil(query.count()/n)

    for page in range(1, pages+1):
        queue.enqueue(index, page, n, timeout=600)


@cli.command()
@click.argument('q')
@click.option('--size', default=10)
@click.option('--start', default=0)
def search(q, size, start):

    """
    Search records.
    """

    results = es.search('hlom', 'record', {
        'size': size,
        'from': start,
        'query': {
            'query_string': {
                'query': q
            }
        },
        'sort': [
            {'count': {'order': 'desc'}},
            '_score'
        ],
        'highlight': {
            'pre_tags': ['\033[1m'],
            'post_tags': ['\033[0m'],
            'fields': {
                '*': {}
            }
        }
    })

    term = Terminal()

    # Total hits.
    hits = str(results['hits']['total'])+' docs'
    click.echo(term.standout_cyan(hits))

    # Print results.
    for hit in results['hits']['hits']:
        click.echo('\n'+term.underline(hit['_id']))
        click.echo(hit['_source']['title'])
        click.echo(hit['_source']['author'])
        click.echo(hit['_source']['stored_id'])
        click.echo(hit['_source']['count'])
