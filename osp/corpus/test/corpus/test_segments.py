

import os

from osp.corpus.segment import Segment
from osp.corpus.corpus import Corpus
from osp.corpus.utils import int_to_dir


def test_full_partition(mock_corpus):

    """
    When no segment boundaries are passed to Corpus#segments(), instances for
    all 4096 segments should be generated.
    """

    # Add all segments.
    mock_corpus.add_segments()
    corpus = Corpus(mock_corpus.path)
    segments = corpus.segments()

    for i in range(0, 4095):

        # Should be a Segment instance.
        segment = next(segments)
        assert isinstance(segment, Segment)

        # Should have the right path.
        dpath = os.path.join(corpus.path, int_to_dir(i))
        assert segment.path == dpath
