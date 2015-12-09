

import pytest

from osp.citations.utils import prettify_field


@pytest.mark.parametrize('raw,pretty', [

    # Strip whitespace.
    ('   abc', 'abc'),
    ('abc   ', 'abc'),

    # Strip punctuation.
    ('.;,abc', 'abc'),
    ('abc.;,', 'abc'),

    # Keep parens.
    ('(abc) def', '(abc) def'),
    ('abc (def)', 'abc (def)'),

])
def test_prettify_field(raw, pretty):
    assert prettify_field(raw) == pretty
