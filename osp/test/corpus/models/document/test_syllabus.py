

from osp.corpus.models import Document
from osp.corpus.syllabus import Syllabus


def test_syllabus(mock_osp):

    """
    Document#syllabus should provide a Syllabus instance bound to the file
    referenced by the document row.
    """

    path = mock_osp.add_file('000', name='123')
    doc = Document(path='000/123')

    assert isinstance(doc.syllabus, Syllabus)
    assert doc.syllabus.path == path
