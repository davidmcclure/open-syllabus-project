

from osp.corpus.segment import Segment


def test_file_names(corpus):

    """
    Segment#file_names() should generate the file names.
    """

    path = corpus.add_segment('000')
    segment = Segment(path)

    # Add 10 files.
    for i in range(0, 10):
        corpus.add_file(segment='000', name='file-'+str(i))

    names = segment.file_names()

    for i in range(0, 10):
        assert next(names) == 'file-'+str(i)
