

import click
import numpy as np
import csv

from osp.common.config import config
from osp.citations.models import Text
from osp.citations.models import Citation
from osp.citations.hlom_corpus import HLOM_Corpus
from osp.citations.jobs import text_to_docs
from peewee import create_model_tables
from playhouse.postgres_ext import ServerSide
from clint.textui.progress import bar


@click.group()
def cli():
    pass


@cli.command()
def init_db():

    """
    Create the database tables.
    """

    create_model_tables([
        Text,
        Citation,
    ], fail_silently=True)


@cli.command()
def ingest_hlom():

    """
    Ingest HLOM texts.
    """

    Text.ingest_hlom()


@cli.command()
def ingest_jstor():

    """
    Ingest JSTOR texts.
    """

    Text.ingest_jstor()
