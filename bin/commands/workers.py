

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


@cli.command()
def queue_doc_to_fields():

    """
    Queue document -> field matching.
    """

    Client().queue(
        'osp.corpus.models.Document',
        'osp.fields.jobs.doc_to_fields',
    )


@cli.command()
def queue_text_to_docs():

    """
    Queue citation extraction.
    """

    Client().queue(
        'osp.citations.models.Text',
        'osp.citations.jobs.text_to_docs',
    )
