

from .conftest import get_config
from rq import Queue


def test_get_rq():

    """
    Config#get_rq() should return a RQ queue.
    """

    config = get_config('get_rq/get-rq')

    rq = config.get_rq()
    assert isinstance(rq, Queue)

    args = rq.connection.connection_pool.connection_kwargs
    assert args['host'] == 'host'
    assert args['port'] == 1337
    assert args['db']   == 1
