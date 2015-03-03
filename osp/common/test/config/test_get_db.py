

from .conftest import get_config


def test_get_database():

    """
    Config#get_db() should return a database object for the requested key.
    """

    config = get_config('get-db-get-database')
    db = config.get_db('test')

    assert db.database                      == 'test-database'
    assert db.connect_kwargs['host']        == 'test-host'
    assert db.connect_kwargs['port']        == 'test-port'
    assert db.connect_kwargs['user']        == 'test-user'
    assert db.connect_kwargs['password']    == 'test-password'


def test_fall_back_on_defaults():

    """
    When the requested key is missing, fall back on the default connection.
    """

    config = get_config('get-db-fall-back-on-defaults')
    db = config.get_db('test')

    assert db.database                      == 'database'
    assert db.connect_kwargs['host']        == 'host'
    assert db.connect_kwargs['port']        == 'port'
    assert db.connect_kwargs['user']        == 'user'
    assert db.connect_kwargs['password']    == 'password'


def test_merge_default_values():

    """
    Before initializing a connection to a non-default host, merge in the
    default values.
    """

    config = get_config('get-db-merge-defaults')
    db = config.get_db('test')

    assert db.database                      == 'database'
    assert db.connect_kwargs['host']        == 'test-host' # overridden
    assert db.connect_kwargs['port']        == 'test-port' # overridden
    assert db.connect_kwargs['user']        == 'user'
    assert db.connect_kwargs['password']    == 'password'
