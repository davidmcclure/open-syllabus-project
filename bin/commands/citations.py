

import click

from elasticsearch import Elasticsearch


@click.group()
def cli():
    pass


@cli.command()
def init_index():

    """
    Initialize the Elasticsearch index.
    """

    # TODO: Env-ify.
    es = Elasticsearch()

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
