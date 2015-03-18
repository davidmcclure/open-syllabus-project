

from .conftest import get_config


def test_top_level_key():

    """
    Config#reset() should restore the value of a top-level key to the original
    value that was loaded from the YAML files.
    """

    config = get_config('reset/top-level')
    config.config.update({'key': 'updated'})
    config.reset()

    assert config['key'] == 'original'


def test_nested_key():

    """
    Nested keys should be restored to the original values.
    """

    config = get_config('reset/nested')
    config.config.update({'key1': { 'key2': 'updated' }})
    config.reset()

    assert config['key1']['key2'] == 'original'
