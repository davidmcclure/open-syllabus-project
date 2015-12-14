

import pytest

from osp.citations.jstor_article import JSTOR_Article


@pytest.mark.parametrize('title,author,queryable', [

    # Title and author.
    ('Article Title', [('David W.', 'McClure')], True),

    # Title and author surname.
    ('Article Title', [('', 'McClure')], True),
    ('Article Title', [(None, 'McClure')], True),

    # Missing title.
    ('', [('David W.', 'McClure')], False),
    (None, [('David W.', 'McClure')], False),

    # Missing author.
    ('Article Title', [], False),

    # Incomplete author.
    ('Article Title', [('David W.', '')], False),
    ('Article Title', [('David W.', None)], False),

])
def test_is_queryable(title, author, queryable, mock_jstor):

    path = mock_jstor.add_article(article_title=title, author=author)

    assert JSTOR_Article(path).is_queryable == queryable
