

import click
import csv
import random

from osp.common.utils import query_bar
from osp.corpus.models import Document
from osp.corpus.models import Document_Text
from peewee import fn


@click.group()
def cli():
    pass


@cli.command()
@click.argument('out_file', type=click.File('w'))
def urls(out_file):

    """
    Write a CSV the URLs for all docs in document_text.
    """

    # CSV writer.
    cols = ['id', 'url']
    writer = csv.DictWriter(out_file, cols)
    writer.writeheader()

    for row in query_bar(Document_Text.select()):

        writer.writerow({
            'id': row.path,
            'url': row.document.syllabus.url,
        })
