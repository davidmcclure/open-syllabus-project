

import pytest

from osp.common.utils import prettify


@pytest.mark.parametrize('ugly,pretty', [

    # Unchanged
    ('The City of God', 'The City of God'),

    # Titlecase
    ('the city of god', 'The City of God'),
    ('THE CITY OF GOD', 'The City of God'),

    # Strip punctuation
    ('The City of God.', 'The City of God'),
    ('The City of God /', 'The City of God'),
    ('The City of God,', 'The City of God'),

    # Strip whitespace
    ('  The City of God  ', 'The City of God'),

    # Keep periods after right-side initials
    ('McClure, David W.', 'McClure, David W.'),
    ('mcclure, david w.', 'McClure, David W.'),

    # Keep right-size parens / brackets.
    ('McClure, D. (David)', 'McClure, D. (David)'),
    ('McClure, D. [David]', 'McClure, D. [David]'),

])
def test_parse_domain(ugly, pretty):
    assert prettify(ugly) == pretty
