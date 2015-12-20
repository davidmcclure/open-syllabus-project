

import click

from blessings import Terminal


def print_code(code):

    """
    Print an HTTP status code.

    Args:
        code (int)
    """

    term = Terminal()

    if code == 200:
        click.echo(term.green(str(code)))

    else:
        click.echo(term.red(str(code)))
