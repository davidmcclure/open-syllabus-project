

import click

from osp.citations.hlom.network import GephiNetwork


@click.group()
def cli():
    pass


@cli.command()
@click.argument('in_file', type=click.Path())
@click.argument('out_file', type=click.Path())
@click.option('--size', type=int, default=10000)
def render(in_file, out_file, size):

    """
    Render the network.
    """

    n = GephiNetwork.from_gexf(in_file)
    n.render(out_file, size=size)
