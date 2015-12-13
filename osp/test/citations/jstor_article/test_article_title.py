

import pytest

from osp.citations.jstor_article import JSTOR_Article


@pytest.mark.parametrize('value,result', [
    ('Test Title', 'Test Title'),
    ('  Test Title  ', 'Test Title'),
    ('', None),
])
def test_article_title(value, result, mock_jstor):

    path = mock_jstor.add_article(article_title=value)

    assert JSTOR_Article(path).article_title == result
