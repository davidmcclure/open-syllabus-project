

import pytest

from osp.citations.models import Text_Index


pytestmark = pytest.mark.usefixtures('db', 'es')


def test_join_citation_count(add_text, add_citation):

    """
    Text_Index.rank_texts() should join the citation count for each text.
    """

    t1 = add_text()
    t2 = add_text()
    t3 = add_text()

    for i in range(2):
        add_citation(t1)

    for i in range(3):
        add_citation(t2)

    for i in range(1):
        add_citation(t3)

    texts = Text_Index.rank_texts()

    assert texts[0].id == t1.id
    assert texts[0].count == 2

    assert texts[1].id == t2.id
    assert texts[1].count == 3

    assert texts[2].id == t3.id
    assert texts[2].count == 1


def test_compute_overall_ranking():
    pass


def test_skip_invalid_citations():
    pass


def test_skip_uncited_texts():
    pass
