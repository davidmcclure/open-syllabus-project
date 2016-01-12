

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

    assert texts[0][0] == t1
    assert texts[0][0].count == 2

    assert texts[1][0] == t2
    assert texts[1][0].count == 3

    assert texts[2][0] == t3
    assert texts[2][0].count == 1


def test_compute_overall_ranking(add_text, add_citation):

    """
    Zip ranks with the texts.
    """

    t1 = add_text()
    t2 = add_text()

    t3 = add_text()
    t4 = add_text()

    t5 = add_text()
    t6 = add_text()

    for i in range(3):
        add_citation(text=t1)
        add_citation(text=t2)

    for i in range(2):
        add_citation(text=t3)
        add_citation(text=t4)

    for i in range(1):
        add_citation(text=t5)
        add_citation(text=t6)

    texts = Text_Index.rank_texts()

    assert texts == [
        (t1, 1),
        (t2, 1),
        (t3, 3),
        (t4, 3),
        (t5, 5),
        (t6, 5),
    ]


def test_skip_invalid_citations(add_text, add_citation):

    """
    Ignore invalid ciatations.
    """

    t1 = add_text()
    t2 = add_text()

    # 1 valid citation.
    add_citation(text=t1, valid=True)
    add_citation(text=t1, valid=False)

    # 0 valid citations.
    add_citation(text=t2, valid=False)

    texts = Text_Index.rank_texts()

    assert texts == [
        (t1, 1),
        # Exclude t2.
    ]


def test_skip_uncited_texts(add_text, add_citation):

    """
    Texts without any citations should be excluded.
    """

    t1 = add_text()
    t2 = add_text()

    add_citation(text=t1, valid=True)

    texts = Text_Index.rank_texts()

    assert texts == [
        (t1, 1),
        # Exclude t2.
    ]
