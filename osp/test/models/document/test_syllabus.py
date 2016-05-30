

import pytest

from osp.models import Document
from osp.corpus.syllabus import Syllabus


pytestmark = pytest.mark.usefixtures('db2')


def test_syllabus(mock_osp):

    """
    Document#syllabus should provide a Syllabus instance for the path.
    """

    path = mock_osp.add_file('000', name='123')

    document = Document(path='000/123')

    assert isinstance(document.syllabus, Syllabus)

    assert document.syllabus.path == path
