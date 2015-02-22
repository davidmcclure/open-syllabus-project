

import click

from osp.common.overview import Overview
from clint.textui.progress import bar


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

    objs = ov.list_objects().json()
    docs = ov.list_documents({'limit': 1000}).json()['items']

    for i in bar(range(1000)):

        links = []
        for j in range(i):
            links.append([docs[j]['id'], objs[j]['id']])

        ov.post_document_objects(links)


@cli.command()
def counts():

    """
    Print the document-object counts.
    """

    print(ov.list_document_object_counts())
