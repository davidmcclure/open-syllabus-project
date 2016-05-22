

import click
import csv

from osp.corpus.models import Document


@click.group()
def cli():
    pass


@cli.command()
@click.argument('in_file', type=click.File('r'))
@click.argument('out_path', type=click.Path())
def pull_docs(in_file, out_path):

    """
    Pull out source documents by database id.
    """

    ids = [int(i.strip()) for i in in_file.readlines()]

    for id in ids:
        row = Document.get(Document.id==id)
        print(row.path)
