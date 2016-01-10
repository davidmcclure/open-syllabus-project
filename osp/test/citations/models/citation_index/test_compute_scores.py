

import pytest
import numpy as np

from osp.citations.models import Citation_Index


pytestmark = pytest.mark.usefixtures('db', 'es')


def test_compute_scores(add_text, add_citation):

    """
    For each text, compute the ratio between the square roots of the text's
    assignment count and the max assignment count.
    """

    t1 = add_text()

    t2 = add_text()
    t3 = add_text()

    t4 = add_text()
    t5 = add_text()
    t6 = add_text()

    for i in range(3):
        add_citation(text=t1)

    for i in range(2):
        add_citation(text=t2)
        add_citation(text=t3)

    for i in range(1):
        add_citation(text=t4)
        add_citation(text=t5)
        add_citation(text=t6)

    Citation_Index.es_insert()

    ranks = Citation_Index.compute_scores()

    assert ranks == {

        str(t1.id): np.sqrt(3) / np.sqrt(3),

        str(t2.id): np.sqrt(2) / np.sqrt(3),
        str(t3.id): np.sqrt(2) / np.sqrt(3),

        str(t4.id): np.sqrt(1) / np.sqrt(3),
        str(t5.id): np.sqrt(1) / np.sqrt(3),
        str(t6.id): np.sqrt(1) / np.sqrt(3),

    }
