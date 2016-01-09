

import click
import multiprocessing as mp
import os

from osp.common import config
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

    workers = {
        'cmd': os.path.join(config['osp']['bin'], 'rqworker'),
        'numprocesses': n,
        'env': {'LANG': 'en_US.UTF-8'}
    }

    arbiter = get_arbiter([workers])

    try:
        arbiter.start()
    finally:
        arbiter.stop()
