

import click

from osp.common.models.base import elasticsearch as es
from osp.corpus.models.text import Document_Text


@click.group()
def cli():
    pass


@cli.command()
def init_index():

    """
    Initialize the index.
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
def count_docs():

    """
    Count documents in the index.
    """

    click.echo(es.count('osp', 'syllabus')['count'])
