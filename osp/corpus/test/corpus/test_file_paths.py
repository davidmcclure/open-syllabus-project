

import os

from osp.corpus.corpus import Corpus
from osp.corpus.utils import int_to_dir


def test_file_paths(mock_corpus):

    """
    Corpus#file_paths() should generate the paths of files in all segments.
    """

    # Add 10 segments.
    mock_corpus.add_segments(s1=0, s2=10)
    corpus = Corpus(mock_corpus.path)

    # Add 10 files per segment.
    for i in range(0, 10):
        segment = int_to_dir(i)
        mock_corpus.add_files(segment, 10, prefix=segment+'-')

    paths = corpus.file_paths()

    # Walk segments:
    for i in range(0, 10):

        segment = int_to_dir(i)

        # Walk files:
        for j in range(0, 10):

            # Should generate the next file path.
            name = segment+'-'+str(j)
            path = os.path.join(corpus.path, segment, name)
            assert next(paths) == path
