

import pytest

from osp.citations.models import Text_Index


pytestmark = pytest.mark.usefixtures('db', 'es')


def test_get_text(add_text, add_citation):

    """
    When a text exists with a given corpus/identifier pair, Text.get_text()
    should return the document.
    """

    t1 = add_text(corpus='hlom', identifier='001-X')
    t2 = add_text(corpus='hlom', identifier='002-X')

    add_citation(text=t1)
    add_citation(text=t2)

    Text_Index.es_insert()

    doc = Text_Index.get_text('hlom', '001-X')

    assert doc['_id'] == str(t1.id)


def test_no_result(add_text, add_citation):

    """
    If no text in the index has the passed corpus/identifier, return None
    """

    t1 = add_text(corpus='hlom', identifier='001-X')

    add_citation(text=t1)

    Text_Index.es_insert()

    doc = Text_Index.get_text('hlom', '002-X')

    assert doc == None
