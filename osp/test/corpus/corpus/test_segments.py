

import os

from osp.corpus.segment import Segment
from osp.corpus.corpus import Corpus
from osp.corpus.utils import int_to_dir


def assert_segment(corpus, segment, offset):

    """
    Check for a well-formed Segment instance.

    Args:
        corpus (Corpus): The parent corpus.
        segment (Segment): The candidate Segment.
        offset (int): The segment offset.
    """

    # Should be a Segment instance.
    assert isinstance(segment, Segment)

    # Should have the correct path.
    dpath = os.path.join(corpus.path, int_to_dir(offset))
    assert segment.path == dpath


def test_full_partition(mock_osp):

    """
    When no segment boundaries are passed to Corpus#segments(), instances for
    all 4096 segments should be generated.
    """

    # Add all segments.
    mock_osp.add_segments()

    # Request all segments.
    corpus = Corpus(mock_osp.path)
    segments = corpus.segments()

    # Should yield all segments.
    for i in range(4095):
        assert_segment(corpus, next(segments), i)

    # But no more.
    assert next(segments, False) == False


def test_bounded_partition(mock_osp):

    """
    When segment boundaries are passed, just the segments that fall within the
    requested range should be provided.
    """

    # Add segments 0-10.
    mock_osp.add_segments(s1=0, s2=10)

    # Request segments 0-10
    corpus = Corpus(mock_osp.path, s1=0, s2=10)
    segments = corpus.segments()

    # Should yield 10 segments.
    for i in range(10):
        assert_segment(corpus, next(segments), i)

    # And then stop.
    assert next(segments, False) == False


def test_missing_segments(mock_osp):

    """
    The generator should gracefully skip missing segments.
    """

    # Add segments 0-10.
    mock_osp.add_segments(s1=0, s2=10)

    # Request segments 0-20.
    corpus = Corpus(mock_osp.path, s1=0, s2=20)
    segments = corpus.segments()

    # Should yield 10 segments.
    for i in range(10):
        assert_segment(corpus, next(segments), i)

    # And then stop.
    assert next(segments, False) == False
