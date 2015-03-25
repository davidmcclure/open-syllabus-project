

import click

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
@click.argument('title')
@click.argument('author')
@click.option('--size', default=10)
@click.option('--start', default=0)
@click.option('--slop', default=2)
def search(title, author, size, start, slop):

    """
    Search documents.
    """

    results = index.es.search('osp', 'syllabus', body={
        'size': size,
        'from': start,
        'fields': [],
        'filter': {
            'and': [
                {
                    'query': {
                        'match_phrase': {
                            'body': {
                                'query': title
                            }
                        }
                    }
                },
                {
                    'query': {
                        'match_phrase': {
                            'body': {
                                'query': author,
                                'slop': 2
                            }
                        }
                    }
                }
            ]
        }
    })

    term = Terminal()

    # Total hits.
    hits = str(results['hits']['total'])+' docs'
    click.echo(term.standout_cyan(hits))
