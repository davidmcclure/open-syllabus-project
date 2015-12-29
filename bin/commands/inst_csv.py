

import click
import csv

from osp.common.utils import query_bar
from osp.institutions.models import Institution
from osp.corpus.models import Document


@click.group()
def cli():
    pass


@cli.command()
@click.argument('out_file', type=click.File('w'))
def orphan_docs(out_file):

    """
    Find document URLs that don't match institutions.
    """

    cols = ['doc', 'url']
    writer = csv.DictWriter(out_file, cols)
    writer.writeheader()

    for doc in query_bar(Document.select()):

        try:

            inst = (
                Institution
                .select()
                .where(Institution.domain==doc.syllabus.domain)
                .first()
            )

            if not inst:
                writer.writerow(dict(
                    doc=doc.path,
                    url=doc.syllabus.url,
                ))

        except:
            pass
