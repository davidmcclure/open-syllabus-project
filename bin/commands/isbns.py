

import click

@click.group()
def cli():
    pass


@cli.command()
def control_to_isbn():

    """
    Map control numbers -> ISBNs.
    """

    print('test')
