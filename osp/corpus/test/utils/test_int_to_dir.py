

from osp.corpus.utils import int_to_dir


def test_convert_int_to_hex():
    """
    Integers should be converted into 3-digit hex values.
    """
    assert int_to_dir(0) == '000'
    assert int_to_dir(16) == '010'
    assert int_to_dir(256) == '100'
