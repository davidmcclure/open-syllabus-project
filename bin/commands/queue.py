

import click
import multiprocessing as mp
import os

from circus import get_arbiter


@click.group()
def cli():
    pass


@cli.command()
@click.option('--n', default=mp.cpu_count())
def work(n):

    """
    Spin up workers.
    """

    workers = {'cmd': os.environ['OSP_WORKER'], 'numprocesses': n}
    arbiter = get_arbiter([workers])

    try:
        arbiter.start()
    finally:
        arbiter.stop()
