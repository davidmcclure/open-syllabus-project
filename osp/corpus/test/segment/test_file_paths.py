

import os

from osp.corpus.segment import Segment


def test_file_paths(corpus):

    """
    Syllabus#file_names() should generate the full file paths.
    """

    path = corpus.add_segment('000')
    segment = Segment(path)

    # Add 10 files.
    for i in range(0, 10):
        corpus.add_file(segment='000', name='file-'+str(i))

    paths = segment.file_paths()

    for i in range(0, 10):
        fpath = os.path.join(path, 'file-'+str(i))
        assert next(paths) == fpath
