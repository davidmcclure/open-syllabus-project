

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

    for url in Inventory().worker_urls:

        # Hit /ping.
        r = requests.get(url+'/ping')

        code = r.status_code
        click.echo(url)

        if code == 200:
            click.echo(term.green('pong'))
        else:
            click.echo(term.red(str(code)))


@cli.command()
def status():

    """
    List the number of pending jobs for each worker.
    """

    urls = [
        'http://localhost:5001',
        'http://localhost:5002'
    ]

    for url in urls:

        # Load rq-dashboard.
        r = requests.get(url+'/rq/queues.json')

        # Find the default queue.
        for queue in r.json()['queues']:
            if queue['name'] == 'default':

                click.echo(url)
                click.echo(term.green(str(queue['count'])))
                break


@cli.command()
def queue_text():

    """
    Queue text extraction.
    """

    urls = Inventory().worker_urls
    pts = partitions(len(urls))

    for i, url in enumerate(urls):

        s1 = pts[i][0]
        s2 = pts[i][1]

        # Post the boundaries.
        r = requests.post(
            url+'/corpus/text',
            params={'s1': s1, 's2': s2 }
        )

        code = r.status_code
        click.echo(url)

        if code == 200:
            click.echo(term.green(str(s1)+'-'+str(s2)))
        else:
            click.echo(term.red(str(code)))
