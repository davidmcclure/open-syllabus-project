

import click
import multiprocessing as mp


@click.group()
def cli():
    pass


@cli.command()
@click.option('--n', default=mp.cpu_count())
def work(n):

    """
    Spin up workers.
    """

    click.echo(n)
