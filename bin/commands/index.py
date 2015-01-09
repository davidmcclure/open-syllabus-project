

import click

from osp.common.models.base import elasticsearch as es
from osp.corpus.models.text import Document_Text as DocText
from clint.textui import progress
from clint.textui import colored
from blessings import Terminal


@click.group()
def cli():
    pass


@cli.command()
def create_index():

    """
    Create the index.
    """

    es.indices.create('osp', {
        'mappings': {
            'syllabus': {
                'properties': {
                    'path': {
                        'type': 'string',
                        'index': 'not_analyzed'
                    },
                    'body': {
                        'type': 'string'
                    }
                }
            }
        }
    })


@cli.command()
def delete_index():

    """
    Delete the index.
    """

    es.indices.delete('osp')


@cli.command()
def count_docs():

    """
    Count documents in the index.
    """

    click.echo(es.count('osp', 'syllabus')['count'])


@cli.command()
def index_docs():

    """
    Index documents.
    """

    # TODO: Use a job queue?
    query = (
        DocText
        .select()
        .distinct([DocText.document])
        .order_by(
            DocText.document,
            DocText.created.desc()
        )
    )

    size = query.count()

    for doc in progress.bar(
        query.naive().iterator(),
        expected_size=size):

        es.index('osp', 'syllabus', {
            'path': doc.document,
            'body': doc.text
        })


@cli.command()
@click.argument('q')
@click.option('--size', default=10)
def search(q, size):

    """
    Search documents.
    """

    results = es.search('osp', 'syllabus', {
        'size': size,
        'fields': ['path'],
        'query': {
            'query_string': {
                'query': q
            }
        },
        'highlight': {
            'pre_tags': ['***'],
            'post_tags': ['***'],
            'fields': {
                'body': {}
            }
        }
    })

    term = Terminal()

    for hit in results['hits']['hits']:
        click.echo(term.bold(hit['fields']['path'][0]))
        for hl in hit['highlight']['body']:
            click.echo(hl)
