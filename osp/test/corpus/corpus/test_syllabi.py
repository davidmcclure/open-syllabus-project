

import os

from osp.corpus.corpus import Corpus
from osp.corpus.syllabus import Syllabus
from osp.test.utils import segment_range


def test_syllabi(mock_osp):

    """
    Corpus#syllabi() should generate Syllabus instances for all files.
    """

    # 10 segments, each with 10 files.
    for s in segment_range(10):
        mock_osp.add_segment(s)
        mock_osp.add_files(s, 10, prefix=s+'-')

    corpus = Corpus(mock_osp.path)
    syllabi = corpus.syllabi()

    # Walk segments / files:
    for s in segment_range(10):
        for i in range(10):

            # Should be a Syllabus instance.
            syllabus = next(syllabi)
            assert isinstance(syllabus, Syllabus)

            # Should generate the next file path.
            name = s+'-'+str(i)
            path = os.path.join(corpus.path, s, name)
            assert syllabus.path == path

    # And stop at the end.
    assert next(syllabi, False) == False
