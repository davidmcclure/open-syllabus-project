

import click

from osp.common.config import config
from osp.corpus.index import CorpusIndex
from blessings import Terminal


index = CorpusIndex()


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
@click.option('--size', default=50)
@click.option('--start', default=0)
@click.option('--slop', default=50)
def search(q, size, start, slop):

    """
    Search documents.
    """

    results = config.es.search('osp', 'syllabus', body={
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
