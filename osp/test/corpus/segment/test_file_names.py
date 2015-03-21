

from osp.corpus.segment import Segment


def test_file_names(mock_osp):

    """
    Segment#file_names() should generate the file names.
    """

    path = mock_osp.add_segment('000')
    segment = Segment(path)

    # Add 10 files.
    for i in range(10):
        mock_osp.add_file(segment='000', name=str(i))

    names = segment.file_names()

    # Should generate file names.
    for i in range(10):
        assert next(names) == str(i)
