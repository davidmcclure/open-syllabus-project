

import csv
import click
import re

from osp.corpus.queries import all_document_texts
from collections import Counter


@click.group()
def cli():
    pass


@cli.command()
@click.argument('out_path', type=click.Path())
@click.option('--limit', default=1000)
@click.option('--skim_depth', default=500)
def csv_depts(out_path, limit, skim_depth):

    """
    Extract "course number" strings to a file.
    """

    out_file = open(out_path, 'w')

    # CSV writer.
    cols = ['dept', 'count']
    writer = csv.DictWriter(out_file, cols)
    writer.writeheader()

    # Limit the text table.
    query = all_document_texts().limit(limit)

    # Match things like "PHYS 101".
    regex = re.compile('(?P<dept>[A-Z]{2,})\s+[0-9]{2,}')

    depts = Counter()
    for doc in query.iterator():

        # Take the first N chars.
        frag = doc.text[:skim_depth]

        # Write the matches to a file.
        for m in re.finditer(regex, frag):
            depts[m.group('dept')] += 1

    # Write the CSV.
    for d in depts.most_common():
        writer.writerow({'dept': d[0], 'count': d[1]})
