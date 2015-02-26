

import pytest

from osp.corpus.utils import tika_is_online, office_to_text


pytestmark = pytest.mark.skipif(
    tika_is_online() == False,
    reason='Tika is offline.'
)


def test_extract_text():

    """
    Text should be extracted via Tika.
    """

    assert True == False
