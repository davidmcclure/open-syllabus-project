

import click

from osp.citations.hlom.models.record import HLOM_Record


@click.group()
def cli():
    pass


@cli.command()
def create():

    """
    Create the HLOM_Record.
    """

    HLOM_Record.es_create()


@cli.command()
def delete():

    """
    Delete the HLOM_Record.
    """

    HLOM_Record.es_delete()


@cli.command()
def reset():

    """
    Reset the HLOM_Record.
    """

    HLOM_Record.es_reset()


@cli.command()
def count():

    """
    Count documents.
    """

    click.echo(HLOM_Record.es_count())


@cli.command()
def insert():

    """
    HLOM_Record documents.
    """

    HLOM_Record.es_insert()
