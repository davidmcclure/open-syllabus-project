

import os
import pytest

from osp.common.config import Config


def get_config(name):

    """
    Load a fixture config file from /fixtures.

    Args:
        name (str): The (base) file name.

    Returns:
        Config: The config instance.
    """

    path = os.path.join(
        os.path.dirname(__file__),
        'fixtures/'+name+'.yml'
    )

    return Config([path])
