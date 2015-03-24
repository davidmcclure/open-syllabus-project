

import click

from osp.citations.hlom.index import HLOMIndex
from blessings import Terminal


index = HLOMIndex()


@click.group()
def cli():
    pass


@cli.command()
def create():

    """
    Create the index.
    """

    index.create()


@cli.command()
def delete():

    """
    Delete the index.
    """

    index.delete()


@cli.command()
def reset():

    """
    Reset the index.
    """

    index.reset()


@cli.command()
def count():

    """
    Count documents.
    """

    click.echo(index.count())


@cli.command()
def insert():

    """
    Index documents.
    """

    index.index()


@cli.command()
@click.argument('q')
@click.option('--size', default=10)
@click.option('--start', default=0)
def search(q, size, start):

    """
    Search records.
    """

    results = index.es.search('hlom', 'record', {
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
