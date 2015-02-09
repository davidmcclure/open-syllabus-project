

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

    for url in Inventory().worker_urls:

        click.echo(url)

        # Load rq-dashboard.
        r = requests.get(url+'/rq/queues.json')

        for queue in r.json()['queues']:

            # Pending jobs:
            if queue['name'] == 'default':
                click.echo(term.green(str(queue['count'])))

            # Failed jobs:
            if queue['name'] == 'failed':
                click.echo(term.red(str(queue['count'])))


@cli.command()
def requeue():

    """
    Requeue all tasks in all workers.
    """

    for url in Inventory().worker_urls:

        # Hit /ping.
        r = requests.post(url+'/rq/requeue-all')

        code = r.status_code
        click.echo(url)

        if code == 200:
            click.echo(term.green(str(code)))
        else:
            click.echo(term.red(str(code)))


@cli.command()
@click.option('--total', default=4095)
def queue_text(total):

    """
    Queue text extraction.
    """

    queue(total, '/corpus/text')


@cli.command()
@click.option('--total', default=10526523)
def queue_hlom(total):

    """
    Queue HLOM citation extraction.
    """

    queue(total, '/hlom/query')


@cli.command()
@click.option('--total', default=4095)
def queue_locate(total):

    """
    Queue doc -> institution matching.
    """

    queue(total, '/locations/locate')


def queue(total, route):

    """
    Queue partitions in EC2 workers.

    :param total: The total number of objects.
    :param route: The API endpoint.
    """

    urls = Inventory().worker_urls
    pts = partitions(total, len(urls))

    for i, url in enumerate(urls):

        o1 = pts[i][0]
        o2 = pts[i][1]

        # Post the boundaries.
        r = requests.post(
            url+route,
            params={'o1': o1, 'o2': o2}
        )

        code = r.status_code
        click.echo(url)

        if code == 200:
            click.echo(term.green(str(o1)+'-'+str(o2)))
        else:
            click.echo(term.red(str(code)))
