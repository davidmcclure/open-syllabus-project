

import click
import requests

from osp.common.inventory import Inventory
from blessings import Terminal


term = Terminal()


@click.group()
def cli():
    pass


@cli.command()
def ping():

    """
    Ping the workers.
    """

    for ip in Inventory().worker_ips:

        # Hit /ping.
        r = requests.get('http://'+ip+'/ping')
        code = r.status_code

        click.echo(ip)
        if code == 200:
            click.echo(term.green('pong'))
        else:
            click.echo(term.red(str(code)))


@cli.command()
def queue_text_extraction():

    """
    Queue text extraction.
    """

    # TODO|dev
    ips = [
        'http://127.0.0.1:5001',
        'http://127.0.0.1:5002'
    ]
