

import os

from osp.corpus.syllabus import Syllabus
from osp.corpus.segment import Segment


def test_syllabi(mock_osp):

    """
    Segment#syllabi() should generate Syllabus instances.
    """

    path = mock_osp.add_segment('000')
    segment = Segment(path)

    # Add 10 files.
    mock_osp.add_files('000', 10)
    syllabi = segment.syllabi()

    for i in range(0, 10):

        # Should be a Syllabus instance.
        syllabus = next(syllabi)
        assert isinstance(syllabus, Syllabus)

        # Should wrap the right file.
        fpath = os.path.join(path, 'file-'+str(i))
        assert syllabus.path == fpath
