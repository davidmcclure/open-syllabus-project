

from .conftest import get_config


def test_get_non_default():

    """
    When the passed table is associated with a custom host, return a
    connection to the custom database.
    """

    config = get_config('get_table_db/get-non-default')
    db = config.get_table_db('remote_table')

    assert db.database                      == 'remote-database'
    assert db.connect_kwargs['host']        == 'remote-host'
    assert db.connect_kwargs['port']        == 'remote-port'
    assert db.connect_kwargs['user']        == 'remote-user'
    assert db.connect_kwargs['password']    == 'remote-password'


def test_fall_back_to_default():

    """
    When the passed table name isn't associated with a custom host, return a
    connection to the default database.
    """

    config = get_config('get_table_db/fall-back-to-default')
    db = config.get_table_db('remote_table')

    assert db.database                      == 'database'
    assert db.connect_kwargs['host']        == 'host'
    assert db.connect_kwargs['port']        == 'port'
    assert db.connect_kwargs['user']        == 'user'
    assert db.connect_kwargs['password']    == 'password'


def test_merge_default_values():

    """
    Before initializing a connection to a custom host, merge the custom
    parameters with the default values.
    """

    config = get_config('get_table_db/merge-default-values')
    db = config.get_table_db('remote_table')

    assert db.database                      == 'database'
    assert db.connect_kwargs['host']        == 'remote-host' # overridden
    assert db.connect_kwargs['port']        == 'remote-port' # overridden
    assert db.connect_kwargs['user']        == 'user'
    assert db.connect_kwargs['password']    == 'password'
