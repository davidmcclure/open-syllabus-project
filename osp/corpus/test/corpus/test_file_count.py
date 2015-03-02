

from osp.corpus.corpus import Corpus
from osp.corpus.utils import int_to_dir


def test_file_count(mock_corpus):

    """
    Corpus#file_count should return the number of files in all segments.
    """

    # Add 10 segments.
    mock_corpus.add_segments(s1=0, s2=10)
    corpus = Corpus(mock_corpus.path)

    # Add 10 files per segment.
    for i in range(0, 10):
        mock_corpus.add_files(int_to_dir(i), 10)

    assert corpus.file_count == 100
