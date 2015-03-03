

from .conftest import get_config


def test_use_custom_connection():

    """
    When the passed table is associated with a custom host, return a
    connection to the custom database.
    """

    config = get_config('get-db-use-custom')

    # Get connection for table linked to `custom1`.
    db = config.get_db('remote_table')

    assert db.database                      == 'remote-database'
    assert db.connect_kwargs['host']        == 'remote-host'
    assert db.connect_kwargs['port']        == 'remote-port'
    assert db.connect_kwargs['user']        == 'remote-user'
    assert db.connect_kwargs['password']    == 'remote-password'


def test_use_default_connection():

    """
    When the passed table name isn't associated with a custom host, return a
    connection to the default database.
    """

    config = get_config('get-db-use-default')

    # Get connection for table without any custom host.
    db = config.get_db('remote_table')

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

    config = get_config('get-db-merge-defaults')

    # Get connection for table linked to `custom2`.
    db = config.get_db('remote_table')

    assert db.database                      == 'database'
    assert db.connect_kwargs['host']        == 'remote-host' # overridden
    assert db.connect_kwargs['port']        == 'remote-port' # overridden
    assert db.connect_kwargs['user']        == 'user'
    assert db.connect_kwargs['password']    == 'password'
