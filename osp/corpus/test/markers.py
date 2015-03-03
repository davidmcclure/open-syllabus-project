

import pytest

from osp.corpus.utils import tika_is_online


requires_tika = pytest.mark.skipif(
    tika_is_online() == False,
    reason='Tika is offline.'
)
