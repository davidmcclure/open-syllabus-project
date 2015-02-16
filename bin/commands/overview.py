

import click
import json

from osp.common.overview import Overview


ov = Overview.from_env()


@click.group()
def cli():
    pass


@cli.command()
def count_objects():

    """
    Print the store object count.
    """

    click.echo(len(ov.list_objects().json()))


@cli.command()
def list_objects():

    """
    Print the store objects.
    """

    objects = ov.list_objects().json()
    click.echo(json.dumps(objects, indent=2))
