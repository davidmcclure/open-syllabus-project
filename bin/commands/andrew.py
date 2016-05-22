

import os
import shutil
import click

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

        path = os.path.join(out_path, row.path)
        dirname = os.path.dirname(path)

        if not os.path.exists(dirname):
            os.makedirs(dirname)

        shutil.copyfile(row.syllabus.path, path)
        shutil.copyfile(row.syllabus.path+'.log', path+'.log')

        print(path)
