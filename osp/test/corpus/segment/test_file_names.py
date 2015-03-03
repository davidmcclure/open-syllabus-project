

from osp.corpus.segment import Segment


def test_file_names(mock_corpus):

    """
    Segment#file_names() should generate the file names.
    """

    path = mock_corpus.add_segment('000')
    segment = Segment(path)

    # Add 10 files.
    mock_corpus.add_files('000', 10)
    names = segment.file_names()

    for i in range(0, 10):
        assert next(names) == 'file-'+str(i)
