

import math
import click
import re

from osp.common.models.base import redis, elasticsearch as es
from osp.citations.hlom.dataset import Dataset
from osp.citations.hlom.models.record import HLOM_Record
from osp.citations.hlom.jobs.index import index
from elasticsearch.helpers import bulk
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
    query = HLOM_Record.select()
    pages = math.ceil(query.count()/n)

    for page in range(1, pages+1):
        queue.enqueue(index, page, n, timeout=600)


@cli.command()
@click.argument('q')
@click.option('--size', default=10)
@click.option('--start', default=0)
@click.option('--slop', default=10)
def search(q, size, start, slop):

    """
    Search records.
    """

    results = es.search('hlom', 'record', {
        'size': size,
        'from': start,
        'fields': [],
        'query': {
            'query_string': {
                'query': q
            }
        },
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

    # Hit highlights.
    for hit in results['hits']['hits']:

        if 'highlight' in hit:
            click.echo('\n'+term.underline(hit['_id']))
            for field, snippets in hit['highlight'].items():
                for snippet in snippets:
                    click.echo(field+': '+snippet)
