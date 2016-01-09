

import pytest

from osp.citations.models import Citation_Index


pytestmark = pytest.mark.usefixtures('db', 'es')


def test_compute_percentiles(add_text, add_citation):

    """
    Text X is assigned more frequently than Y% of all texts.
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

    Citation_Index.es_insert()

    ranks = Citation_Index.compute_percentiles()

    assert ranks == {
        str(t1.id): 4/6,
        str(t2.id): 4/6,
        str(t3.id): 2/6,
        str(t4.id): 2/6,
        str(t5.id): 0,
        str(t6.id): 0,
    }
