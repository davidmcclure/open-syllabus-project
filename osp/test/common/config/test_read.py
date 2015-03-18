

from .conftest import get_config


def test_read_on_startup():

    """
    Config should call read() when an instance is created.
    """

    config = get_config('read/read')
    assert config['key'] == 'original'


def test_revert_changes():

    """
    If read() is called on an existing instance, the configuration files
    should be reloaded, reverting any changes to the values.
    """

    config = get_config('read/read')
    config.config.update({'key': 'updated'})
    config.read()

    assert config['key'] == 'original'
