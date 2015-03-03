

from osp.corpus.syllabus import Syllabus


def test_file_name(mock_corpus):

    """
    Syllabus#file_name Should return the base file name.
    """

    path = mock_corpus.add_file(name='name')
    syllabus = Syllabus(path)

    assert syllabus.file_name == 'name'
