

from osp.corpus.syllabus import Syllabus


def test_relative_path(corpus):

    """
    Syllabys#relative_path should return the corpus-relative path.
    """

    path = corpus.add_file(segment='segment', name='name')
    syllabus = Syllabus(path)

    assert syllabus.relative_path == 'segment/name'
