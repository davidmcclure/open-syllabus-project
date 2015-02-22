

import click

from osp.common.overview import Overview


ov = Overview.from_env()


@click.group()
def cli():
    pass


@cli.command()
def push_objects():

    """
    Push test store objects.
    """

    objects = []
    for i in range(1000):
        objects.append({
            'indexedLong': i,
            'indexedString': None,
            'json': {}
        })

    ov.post_object(objects)


@cli.command()
def push_document_objects():

    """
    Print the document-store objects.
    """

    objects = ov.list_objects().json()
    documents = ov.list_documents({'limit': 1000})
    print(documents)
