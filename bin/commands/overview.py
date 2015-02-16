

import click
from osp.common.overview import Overview


ov = Overview.from_env()


@click.group()
def cli():
    pass


@cli.command()
def object_count():

    """
    Print the store object count.
    """

    click.echo(len(ov.list_objects().json()))


@cli.command()
def list_objects():

    """
    Print the store object count.
    """

    click.echo(ov.list_objects().json())
