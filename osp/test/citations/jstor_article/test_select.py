

import pytest

from osp.citations.jstor_article import JSTOR_Article


@pytest.mark.parametrize('value,result', [
    ('12345', '12345'),
    ('  12345  ', '12345'),
    ('', None),
])
def test_select(value, result, mock_jstor):

    path = mock_jstor.add_article(article_id=value)

    assert JSTOR_Article(path).select('article-id') == result
