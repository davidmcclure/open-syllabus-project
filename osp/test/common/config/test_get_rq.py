

from .conftest import get_config


def test_get_rq():

    """
    Config#get_rq() should return a RQ queue.
    """

    config = get_config('get_rq/get-rq')
    queue = config.get_rq()

    args = queue.connection.connection_pool.connection_kwargs

    assert args['host'] == 'host'
    assert args['port'] == 1337
    assert args['db']   == 1
