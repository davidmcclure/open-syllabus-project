

import click

from osp.workers.client import Client


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


@cli.command()
def queue_doc_to_inst():

    """
    Queue document -> institution matching.
    """

    Client().queue(
        'osp.corpus.models.Document',
        'osp.institutions.jobs.doc_to_inst',
    )
