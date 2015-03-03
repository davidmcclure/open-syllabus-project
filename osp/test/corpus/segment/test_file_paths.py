

import os

from osp.corpus.segment import Segment


def test_file_paths(mock_corpus):

    """
    Segment#file_names() should generate the full file paths.
    """

    path = mock_corpus.add_segment('000')
    segment = Segment(path)

    # Add 10 files.
    mock_corpus.add_files('000', 10)
    paths = segment.file_paths()

    for i in range(0, 10):
        fpath = os.path.join(path, 'file-'+str(i))
        assert next(paths) == fpath
