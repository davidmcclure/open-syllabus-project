

import pytest

from osp.citations.jstor_article import JSTOR_Article


@pytest.mark.parametrize('value,result', [

    ('Article Title', 'Article Title'),

    # Strip whitespace.
    ('  Article Title  ', 'Article Title'),

    # Empty tag -> None.
    ('', None),

    # Missing tag -> None.
    (None, None),

])
def test_select(value, result, mock_jstor):

    path = mock_jstor.add_article(article_title=value)

    assert JSTOR_Article(path).select('article-title') == result
