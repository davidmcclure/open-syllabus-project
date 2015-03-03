

import os
import pytest

from osp.common.config import Config


def get_path(name):

    """
    Get the path of a config file in /fixtures.

    Args:
        name (str): The (base) file name.

    Returns:
        str: The file path.
    """

    return os.path.join(
        os.path.dirname(__file__),
        'fixtures/'+name+'.yml'
    )


def get_config(*names):

    """
    Load a fixture config file from /fixtures.

    Args:
        name (str): The (base) file name.

    Returns:
        Config: The config instance.
    """

    paths = list(map(get_path, names))
    return Config(paths)
