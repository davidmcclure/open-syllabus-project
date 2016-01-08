

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
    ('The City of God,/', 'The City of God'),

    # Strip whitespace
    ('  The City of God  ', 'The City of God'),

])
def test_parse_domain(ugly, pretty):
    assert prettify(ugly) == pretty
