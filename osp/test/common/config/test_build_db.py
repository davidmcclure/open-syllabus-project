

from .conftest import get_config


def test_default_to_default():

    """
    When no name is passed to Config#build_db(), use the default connection.
    """

    config = get_config('build_db/default')
    db = config.build_db()

    assert db.database                      == 'database'
    assert db.connect_kwargs['host']        == 'host'
    assert db.connect_kwargs['port']        == 'port'
    assert db.connect_kwargs['user']        == 'user'
    assert db.connect_kwargs['password']    == 'password'


def test_fall_back_to_default():

    """
    If the configuration doesn't have an entry for the requested host, fall
    back on the default connection.
    """

    config = get_config('build_db/default')
    db = config.build_db('test')

    assert db.database                      == 'database'
    assert db.connect_kwargs['host']        == 'host'
    assert db.connect_kwargs['port']        == 'port'
    assert db.connect_kwargs['user']        == 'user'
    assert db.connect_kwargs['password']    == 'password'


def test_get_non_default():

    """
    Config#build_db() should return a database object for the requested key.
    """

    config = get_config('build_db/non-default')
    db = config.build_db('test')

    assert db.database                      == 'test-database'
    assert db.connect_kwargs['host']        == 'test-host'
    assert db.connect_kwargs['port']        == 'test-port'
    assert db.connect_kwargs['user']        == 'test-user'
    assert db.connect_kwargs['password']    == 'test-password'


def test_merge_default_values():

    """
    Before initializing a connection to a non-default host, merge in the
    default values. (This makes it possible to just override the values that
    are different in the custom host.)
    """

    config = get_config('build_db/merge')
    db = config.build_db('test')

    assert db.database                      == 'database'
    assert db.connect_kwargs['host']        == 'test-host' # overridden
    assert db.connect_kwargs['port']        == 'test-port' # overridden
    assert db.connect_kwargs['user']        == 'user'
    assert db.connect_kwargs['password']    == 'password'
