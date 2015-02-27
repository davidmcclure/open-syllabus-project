

from osp.corpus.syllabus import Syllabus


def test_open(corpus):

    """
    Syllabys#open() should provide a file handle.
    """

    path = corpus.add_file(name='name')
    syllabus = Syllabus(path)

    with syllabus.open() as fh:
        assert fh.name == path
        assert fh.mode == 'rb'
