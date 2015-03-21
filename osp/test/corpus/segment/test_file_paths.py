

import os

from osp.corpus.segment import Segment


def test_file_paths(mock_osp):

    """
    Segment#file_names() should generate the full file paths.
    """

    path = mock_osp.add_segment('000')
    segment = Segment(path)

    # Add 10 files.
    for i in range(10):
        mock_osp.add_file(segment='000', name=str(i))

    paths = segment.file_paths()

    # Should generate file paths.
    for i in range(10):
        fpath = os.path.join(path, str(i))
        assert next(paths) == fpath
