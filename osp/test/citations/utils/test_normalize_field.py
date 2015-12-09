

import pytest

from osp.citations.utils import normalize_field


@pytest.mark.parametrize('raw,normalized', [

    # Remove punctuation.
    ('Antonio (Flaminio),', 'antonio flaminio'),

    # Remove numbers.
    ('Keats, John, 1795-1821', 'keats john')

])
def test_sanitize_query(raw, normalized):
    assert normalize_field(raw) == normalized
