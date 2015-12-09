

import pytest

from osp.citations.utils import sanitize_query


@pytest.mark.parametrize('raw,sanitized', [

    # Remove punctuation.
    ('Antonio (Flaminio),', 'antonio flaminio'),

    # Remove numbers.
    ('Keats, John, 1795-1821', 'keats john')

])
def test_sanitize_query(raw, sanitized):
    assert sanitize_query(raw) == sanitized
