

from osp.corpus.segment import Segment


def test_file_count(corpus):

    """
    Syllabus#file_count() should return the number of files.
    """

    path = corpus.add_segment('000')
    segment = Segment(path)

    # Add 10 files.
    for i in range(0, 10):
        corpus.add_file(segment='000', name='file-'+str(i))

    assert segment.file_count == 10
