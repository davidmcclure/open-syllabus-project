

import click
import math

from osp.common.utils import query_bar
from osp.common.models.base import elasticsearch as es
from osp.corpus.models.text import Document_Text
from elasticsearch.helpers import bulk
from playhouse.postgres_ext import ServerSide
from blessings import Terminal


@click.group()
def cli():
    pass


@cli.command()
def create():

    """
    Create the index.
    """

    Document_Text.es_create()


@cli.command()
def delete():

    """
    Delete the index.
    """

    Document_Text.es_delete()


@cli.command()
def count():

    """
    Count documents.
    """

    click.echo(Document_Text.es_count())


@cli.command()
def insert():

    """
    Index documents.
    """

    Document_Text.es_index()


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
