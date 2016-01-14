

import pytest

from osp.citations.models import Text


pytestmark = pytest.mark.usefixtures('db')


def test_select_cited(add_text, add_citation):

    """
    Text.select_cited() returns texts that have been cited at least once.
    """

    t1 = add_text()
    t2 = add_text()
    t3 = add_text()

    add_citation(text=t1)
    add_citation(text=t2)
    # No citation for t3

    assert list(Text.select_cited()) == [
        t1,
        t2,
    ]
