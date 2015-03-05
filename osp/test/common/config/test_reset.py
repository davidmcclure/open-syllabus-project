

from .conftest import get_config


def test_reset():

    """
    Config#reset() should return the config to the original values that were
    loaded from the YAML files.
    """

    config = get_config('reset/reset')
    config.config.update({'key': 'updated'})
    config.reset()

    assert config['key'] == 'original'
