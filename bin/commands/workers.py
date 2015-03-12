

import click
import requests

from osp.common.utils import partitions
from osp.common.inventory import Inventory
from osp.corpus.models.document import Document
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

        # Get the queue counts.
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
@click.argument('max_id', type=int)
def queue_text(max_id):

    """
    Queue text extraction.
    """

    queue('/corpus/text', max_id)


@cli.command()
@click.argument('max_id', type=int)
def queue_date_archive_url(max_id):

    """
    Queue date archive URL extraction.
    """

    queue('/dates/archive-url', max_id)


@cli.command()
@click.argument('max_id', type=int)
def queue_date_semester(max_id):

    """
    Queue date semester extraction.
    """

    queue('/dates/semester', max_id)


def queue(route, max_id):

    """
    Queue partitions in EC2 workers.

    Args:
        route (str): The API endpoint.
        max_id (int): The highest ID.
    """

    urls = Inventory().worker_urls
    pts = partitions(1, max_id, len(urls))

    for i, url in enumerate(urls):

        o1 = pts[i][0]
        o2 = pts[i][1]

        # Post the boundaries.
        r = requests.post(
            url+route,
            data={'o1': o1, 'o2': o2}
        )

        code = r.status_code
        click.echo(url)

        if code == 200:
            click.echo(term.green(str(o1)+'-'+str(o2)))
        else:
            click.echo(term.red(str(code)))
