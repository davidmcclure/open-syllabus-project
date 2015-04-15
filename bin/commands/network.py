

import click

from osp.citations.hlom.network import GephiNetwork


@click.group()
def cli():
    pass


@cli.command()
@click.argument('in_file', type=click.Path())
@click.argument('out_file', type=click.Path())
@click.option('--scale', type=int, default=5)
@click.option('--size', type=int, default=320000)
@click.option('--font_size', type=int, default=14)
def render(in_file, out_file, scale, size, font_size):

    """
    Render the network.
    """

    n = GephiNetwork.from_gexf(in_file)
    n.render(out_file, scale=scale, size=size, font_size=font_size)
