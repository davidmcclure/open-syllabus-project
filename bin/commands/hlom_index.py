

import click

from osp.common.models.base import elasticsearch as es
from osp.citations.hlom.dataset import Dataset


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
