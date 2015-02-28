

from osp.corpus.segment import Segment


def test_file_count(corpus):

    """
    Segment#file_count() should return the number of files.
    """

    path = corpus.add_segment('000')
    segment = Segment(path)

    # Add 10 files.
    corpus.add_files('000', 10)
    assert segment.file_count == 10
