

from .conftest import get_config


def test_get_es():

    """
    Config#get_es() should return an Elasticsearch connection.
    """

    config = get_config('get_es/get-es')
    es = config.get_es()

    args = es.transport.hosts[0]

    assert args['host'] == 'host'
    assert args['port'] == 1337
