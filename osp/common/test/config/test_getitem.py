

import os

from osp.common.config import Config
from .conftest import get_config


def test_getitem():

    """
    It should be possible to access keys in the underlying anyconfig instance
    by indexing an instance of Config.
    """

    config = get_config('getitem')

    assert config['key1'] == 'val1'
    assert config['key2'] == 'val2'
