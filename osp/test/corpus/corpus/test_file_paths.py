

import os

from osp.corpus.corpus import Corpus
from osp.test.utils import segment_range


def test_file_paths(mock_corpus):

    """
    Corpus#file_paths() should generate the paths of files in all segments.
    """

    # 10 segments, each with 10 files.
    for s in segment_range(0, 10):
        mock_corpus.add_segment(s)
        mock_corpus.add_files(s, 10, prefix=s+'-')

    corpus = Corpus(mock_corpus.path)
    paths = corpus.file_paths()

    # Walk segments / files:
    for s in segment_range(0, 10):
        for i in range(0, 10):

            # Should generate the next file path.
            name = s+'-'+str(i)
            path = os.path.join(corpus.path, s, name)
            assert next(paths) == path

    # And stop at the end.
    assert next(paths, False) == False
