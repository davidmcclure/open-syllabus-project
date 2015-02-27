

import os

from osp.corpus.segment import Segment


def test_file_names(corpus):

    """
    Segment#file_names() should generate a list of file names.
    """

    path = corpus.add_segment('000')
    segment = Segment(path)
    corpus.add_files('000', 10)

    names = segment.file_names

    for i in range(0, 10):
        assert next(names) == 'file-'+str(i)
