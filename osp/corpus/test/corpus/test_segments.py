

from osp.corpus.segment import Segment
from osp.corpus.corpus import Corpus


def test_full_partition(mock_corpus):

    """
    When no segments are passed to Corpus#segments(), instances for all 4096
    segments should be generated.
    """

    # All all segments.
    mock_corpus.add_segments()
