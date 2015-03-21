

import os

from osp.corpus.corpus import Corpus
from osp.test.utils import segment_range


def test_file_paths(mock_osp):

    """
    Corpus#file_paths() should generate the paths of files in all segments.
    """

    # 10 segments, each with 10 files.
    for s in segment_range(10):
        for i in range(10):
            mock_osp.add_file(segment=s, name=s+'-'+str(i))

    corpus = Corpus(mock_osp.path)
    paths = corpus.file_paths()

    # Walk segments / files:
    for s in segment_range(10):
        for i in range(10):

            # Should generate the next file path.
            name = s+'-'+str(i)
            path = os.path.join(corpus.path, s, name)
            assert next(paths) == path

    # And stop at the end.
    assert next(paths, False) == False
