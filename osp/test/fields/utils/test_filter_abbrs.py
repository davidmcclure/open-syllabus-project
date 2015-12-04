

from osp.fields.utils import filter_abbrs


def test_filter_abbrs():

    """
    filter_abbrs() should remove blacklisted abbreviations.
    """

    filtered = filter_abbrs(
        ['AB', 'CD', 'EF', 'GH'], ['CD', 'GH']
    )

    assert filtered == ['AB', 'EF']
