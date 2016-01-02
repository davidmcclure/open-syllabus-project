

import pytest

from osp.citations.jstor_record import JSTOR_Record


@pytest.mark.parametrize('title,author,queryable', [

    # Title and full author.
    ('Article Title', [('David W.', 'McClure')], True),

    # Title and surname.
    ('Article Title', [('', 'McClure')], True),
    ('Article Title', [(None, 'McClure')], True),

    # Missing title.
    ('', [('David W.', 'McClure')], False),
    (None, [('David W.', 'McClure')], False),

    # Missing author.
    ('Article Title', [], False),

    # Missing surname.
    ('Article Title', [('David W.', '')], False),
    ('Article Title', [('David W.', None)], False),

    # Missing title and author.
    ('', [], False),
    (None, [], False),

])
def test_is_queryable(title, author, queryable, mock_jstor):

    path = mock_jstor.add_article(article_title=title, author=author)

    assert JSTOR_Record(path).is_queryable == queryable
