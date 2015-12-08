

import click

from osp.api.client import Client


@click.group()
def cli():
    pass


@cli.command()
def ping():

    """
    Ping the workers.
    """

    Client().ping()


@cli.command()
def status():

    """
    Print queue counts.
    """

    Client().status()


@cli.command()
def clear():

    """
    Clear all queues.
    """

    Client().clear()


@cli.command()
def requeue():

    """
    Requeue failed jobs.
    """

    Client().requeue()


@cli.command()
def queue_ext_text():

    """
    Queue text extraction.
    """

    Client().queue(
        'osp.corpus.models.Document',
        'osp.corpus.jobs.ext_text',
    )








# @cli.command()
# def status():

    # """
    # List the number of pending jobs for each worker.
    # """

    # for url in Inventory().worker_urls:

        # click.echo(url)

        # # Get the queue counts.
        # r = requests.get(url+'/rq/queues.json')

        # for queue in r.json()['queues']:

            # # Pending jobs:
            # if queue['name'] == 'default':
                # click.echo(term.green(str(queue['count'])))

            # # Failed jobs:
            # if queue['name'] == 'failed':
                # click.echo(term.red(str(queue['count'])))


# @cli.command()
# def requeue():

    # """
    # Requeue all tasks in all workers.
    # """

    # for url in Inventory().worker_urls:

        # click.echo(url)

        # # Hit /ping.
        # r = requests.post(url+'/rq/requeue-all')
        # print_code(r.status_code)


# @cli.command()
# def reset():

    # """
    # Clear `default` and `failed` queues on all workers.
    # """

    # for url in Inventory().worker_urls:

        # click.echo(url)

        # # Default:
        # r1 = requests.post(url+'/rq/queue/default/empty')
        # print_code(r1.status_code)

        # # Failed:
        # r2 = requests.post(url+'/rq/queue/failed/empty')
        # print_code(r2.status_code)


# @cli.command()
# @click.argument('max_id', type=int)
# def queue_corpus_text(max_id):

    # """
    # Queue text extraction.
    # """

    # queue('/corpus/text', max_id)


# @cli.command()
# @click.argument('max_id', type=int)
# def queue_date_archive_url(max_id):

    # """
    # Queue archive URL date extraction.
    # """

    # queue('/dates/archive-url', max_id)


# @cli.command()
# @click.argument('max_id', type=int)
# def queue_date_semester(max_id):

    # """
    # Queue semester date extraction.
    # """

    # queue('/dates/semester', max_id)


# @cli.command()
# @click.argument('max_id', type=int)
# def queue_date_file_metadata(max_id):

    # """
    # Queue file metadata date extraction.
    # """

    # queue('/dates/file-metadata', max_id)


# @cli.command()
# @click.argument('max_id', type=int)
# def queue_hlom_query(max_id):

    # """
    # Queue HLOM queries.
    # """

    # queue('/hlom/query', max_id)


# @cli.command()
# @click.argument('max_id', type=int)
# def queue_match_doc_inst(max_id):

    # """
    # Queue document -> institution queries.
    # """

    # queue('/locations/match-doc', max_id)


# def queue(route, max_id):

    # """
    # Queue partitions in EC2 workers.

    # Args:
        # route (str): The API endpoint.
        # max_id (int): The highest ID.
    # """

    # urls = Inventory().worker_urls
    # pts = partitions(1, max_id, len(urls))

    # for i, url in enumerate(urls):

        # o1 = pts[i][0]
        # o2 = pts[i][1]

        # # Post the boundaries.
        # r = requests.post(
            # url+route,
            # data={'o1': o1, 'o2': o2}
        # )

        # code = r.status_code
        # click.echo(url)

        # if code == 200:
            # click.echo(term.green(str(o1)+'-'+str(o2)))
        # else:
            # click.echo(term.red(str(code)))


# def print_code(code):

    # """
    # Print a colored status code.
    # """

    # if code == 200:
        # click.echo(term.green('200'))
    # else:
        # click.echo(term.red(str(code)))
