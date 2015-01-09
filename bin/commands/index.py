

import click
import math

from osp.common.models.base import elasticsearch as es
from osp.corpus.models.text import Document_Text as DocText
from elasticsearch.helpers import bulk
from clint.textui import colored
from clint.textui.progress import bar
from blessings import Terminal


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
@click.option('--page', default=10000)
def insert(page):

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

    # Iterate over pages.
    pages = math.ceil(query.count()/page)
    for p in bar(range(1, pages+1)):

        paginated = query.paginate(p, page).iterator()

        docs = []
        for doc in paginated:
            docs.append({
                'path': doc.document,
                'body': doc.text
            })

        # Bulk-index the page.
        bulk(es, docs, index='osp', doc_type='syllabus')


@cli.command()
@click.argument('q')
@click.option('--size', default=10)
def search(q, size):

    """
    Search documents.
    """

    # Query ES.
    results = es.search('osp', 'syllabus', {
        'size': size,
        'fields': ['path'],
        'query': {
            'query_string': {
                'query': q
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

    # Print results.
    for hit in results['hits']['hits']:
        click.echo(term.bold(hit['fields']['path'][0]))
        for hl in hit['highlight']['body']:
            click.echo(hl)
