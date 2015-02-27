

from osp.corpus.syllabus import Syllabus


def test_file_name(corpus):

    """
    Syllabus#file_name Should return the base file name.
    """

    path = corpus.add_file(name='name')
    syllabus = Syllabus(path)

    assert syllabus.file_name == 'name'
