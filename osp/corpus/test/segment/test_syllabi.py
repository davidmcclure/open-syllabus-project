

import os

from osp.corpus.syllabus import Syllabus
from osp.corpus.segment import Segment


def test_syllabi(corpus):

    """
    Segment#syllabi() should generate Syllabus instances.
    """

    path = corpus.add_segment('000')
    segment = Segment(path)

    # Add 10 files.
    for i in range(0, 10):
        corpus.add_file(segment='000', name='file-'+str(i))

    syllabi = segment.syllabi()

    for i in range(0, 10):

        syllabus = next(syllabi)
        assert isinstance(syllabus, Syllabus)

        fpath = os.path.join(path, 'file-'+str(i))
        assert syllabus.path == fpath
