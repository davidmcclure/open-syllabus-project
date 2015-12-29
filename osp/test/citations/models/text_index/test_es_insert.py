

import pytest

from osp.common.config import config
from osp.citations.models import Text_Index
from osp.citations.models import Text


pytestmark = pytest.mark.usefixtures('db', 'es')


def test_es_insert(add_text):

    """
    Text_Index.es_insert() should index texts.
    """

    for i in map(str, range(10)):
        add_text(
            title       = 'title'+i,
            author      = ['author1'+i, 'author2'+i],
            publisher   = 'publisher'+i,
            date        = 'date'+i,
            journal     = 'journal'+i,
            url         = 'url'+i,
        )

    Text_Index.es_insert()

    for text in Text.select():

        doc = config.es.get(
            index='text',
            id=text.id,
        )

        assert doc['_source']['title'] == text.title
        assert doc['_source']['author'] == text.author
        assert doc['_source']['publisher'] == text.publisher
        assert doc['_source']['date'] == text.date
        assert doc['_source']['journal'] == text.journal_title
        assert doc['_source']['url'] == text.url
