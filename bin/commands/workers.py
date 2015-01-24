

import click
import requests

from osp.common.utils import partitions
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

    for ip in Inventory().worker_urls:

        # Hit /ping.
        r = requests.get(ip+'/ping')

        code = r.status_code
        click.echo(ip)

        if code == 200:
            click.echo(term.green('pong'))
        else:
            click.echo(term.red(str(code)))


@cli.command()
def queue_text():

    """
    Queue text extraction.
    """

    urls = Inventory().worker_urls
    pts = partitions(len(urls))

    for i, ip in enumerate(ips):

        s1 = pts[i][0]
        s2 = pts[i][1]

        r = requests.post(
            ip+'/corpus/text',
            params={'s1': s1, 's2': s2 }
        )

        code = r.status_code
        click.echo(ip)

        if code == 200:
            click.echo(term.green(str(s1)+'-'+str(s2)))
        else:
            click.echo(term.red(str(code)))
