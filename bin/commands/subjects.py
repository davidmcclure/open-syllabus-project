

import click
import re

from osp.corpus.queries import all_document_texts
from osp.common.utils import paginate_query


@click.group()
def cli():
    pass


@cli.command()
@click.argument('out_path', type=click.Path())
@click.option('--page_len', default=1000)
@click.option('--skim_depth', default=500)
def course_numbers(out_path, page_len, skim_depth):

    """
    Extract "course number" strings to a file.
    """

    query = all_document_texts()
    pages = paginate_query(query, page_len, bar=True)
    out_file = open(out_path, 'w')

    # Match things like "PHYS 101".
    regex = re.compile('[A-Z]{2,}\s+[0-9]{2,}')

    for page in pages:
        for doc in page.iterator():

            # Take the first N chars.
            frag = doc.text[:skim_depth]

            # Write the matches to a file.
            for match in re.findall(regex, frag):
                print(match, file=out_file)
