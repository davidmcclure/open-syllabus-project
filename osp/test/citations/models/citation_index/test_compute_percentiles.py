

import pytest

from osp.citations.models import Citation_Index


pytestmark = pytest.mark.usefixtures('db', 'es')


def test_compute_percentiles(add_text, add_citation):

    """
    Text X is assigned more frequently than Y% of all texts.
    """

    pass
