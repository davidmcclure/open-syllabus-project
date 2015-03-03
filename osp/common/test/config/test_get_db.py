

from .conftest import get_config


def test_use_custom_connection():

    """
    When the passed table is associated with a custom host, return a
    connection to the custom database.
    """

    config = get_config('get-db')

    # Get connection for table linked to `custom1`.
    db = config.get_db('table1')

    assert db.database                      == 'c1-database'
    assert db.connect_kwargs['host']        == 'c1-host'
    assert db.connect_kwargs['port']        == 'c1-port'
    assert db.connect_kwargs['user']        == 'c1-user'
    assert db.connect_kwargs['password']    == 'c1-password'


def test_use_default_connection():

    """
    When the passed table name isn't associated with a custom host, return a
    connection to the default database.
    """

    config = get_config('get-db')

    # Get connection for table without any custom host.
    db = config.get_db('table3')

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

    config = get_config('get-db')

    # Get connection for table linked to `custom2`.
    db = config.get_db('table2')

    assert db.database                      == 'database'
    assert db.connect_kwargs['host']        == 'c2-host' # overridden
    assert db.connect_kwargs['port']        == 'c2-port' # overridden
    assert db.connect_kwargs['user']        == 'user'
    assert db.connect_kwargs['password']    == 'password'
