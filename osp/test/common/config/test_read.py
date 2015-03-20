

from .conftest import get_config, get_path
from rq import Queue
from elasticsearch import Elasticsearch


def test_read_defaults():

    """
    When initialized, Config should read the default paths and expose the
    underlying configuration object.
    """

    config = get_config('read/default')

    assert config['key1'] == 'val1'
    assert config['key2'] == 'val2'


def test_revert_changes():

    """
    If read() is called on an existing instance, the configuration files
    should be reloaded, reverting any changes to the values.
    """

    config = get_config('read/revert')
    config.config.update({'key': 'updated'})
    config.read()

    assert config['key'] == 'original'


def test_set_es():

    """
    When Elasticsearch params are provided, set a connection instance.
    """

    config = get_config('read/set-es')

    # Should set an instance.
    assert isinstance(config.es, Elasticsearch)

    args = config.es.transport.hosts[0]

    # Should use config args.
    assert args['host'] == 'host'
    assert args['port'] == 1337


def test_set_rq():

    """
    When Redis params are provided, set an RQ instance.
    """

    config = get_config('read/set-rq')

    # Should set an instance.
    assert isinstance(config.rq, Queue)

    args = config.rq.connection.connection_pool.connection_kwargs

    # Should use config args.
    assert args['host'] == 'host'
    assert args['port'] == 1337
    assert args['db']   == 1
