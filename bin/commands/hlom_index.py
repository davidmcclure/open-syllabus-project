

import click

from osp.citations.hlom.index import HLOMIndex


index = HLOMIndex()


@click.group()
def cli():
    pass


@cli.command()
def create():

    """
    Create the index.
    """

    index.create()


@cli.command()
def delete():

    """
    Delete the index.
    """

    index.delete()


@cli.command()
def reset():

    """
    Reset the index.
    """

    index.reset()


@cli.command()
def count():

    """
    Count documents.
    """

    click.echo(index.count())


@cli.command()
def insert():

    """
    Index documents.
    """

    index.index()
