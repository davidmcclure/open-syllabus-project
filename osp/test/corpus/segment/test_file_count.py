

from osp.corpus.segment import Segment


def test_file_count(mock_osp):

    """
    Segment#file_count() should return the number of files.
    """

    path = mock_osp.add_segment('000')
    segment = Segment(path)

    # Add 10 files.
    for i in range(10):
        mock_osp.add_file(segment='000', name=str(i))

    # Should count 10 files.
    assert segment.file_count == 10
