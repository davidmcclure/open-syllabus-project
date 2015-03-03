

from osp.corpus.syllabus import Syllabus


def test_segment_name(mock_corpus):

    """
    Syllabys#segment_name should return the segment directory name.
    """

    path = mock_corpus.add_file(segment='001')
    syllabus = Syllabus(path)

    assert syllabus.segment_name == '001'
