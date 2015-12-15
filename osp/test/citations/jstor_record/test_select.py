

import pytest

from osp.citations.jstor_record import JSTOR_Record


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

    assert JSTOR_Record(path).select('article-title') == result
