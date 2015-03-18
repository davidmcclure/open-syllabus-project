

from .conftest import get_config
from elasticsearch import Elasticsearch


def test_get_es():

    """
    Config#es should return an Elasticsearch connection.
    """

    config = get_config('get_es/get-es')

    es = config.get_es()
    assert isinstance(es, Elasticsearch)

    args = es.transport.hosts[0]
    assert args['host'] == 'host'
    assert args['port'] == 1337
