

from osp.corpus.syllabus import Syllabus
from osp.test.utils import requires_tika


def test_empty(mock_osp):

    """
    Should return None if the file is empty.
    """

    path = mock_osp.add_file(content='', ftype='plain')
    syllabus = Syllabus(path)

    assert syllabus.text() == None


def test_plaintext(mock_osp):

    """
    Should extract text from vanilla text files.
    """

    path = mock_osp.add_file(content='text', ftype='plain')
    syllabus = Syllabus(path)

    assert syllabus.text() == 'text'


def test_html(mock_osp):

    """
    Should extract text from HTML files.
    """

    path = mock_osp.add_file(content='<p>text</p>', ftype='html')
    syllabus = Syllabus(path)

    assert syllabus.text() == 'text'


def test_pdf(mock_osp):

    """
    Should extract text from PDF files.
    """

    path = mock_osp.add_file(content='text', ftype='pdf')
    syllabus = Syllabus(path)

    assert syllabus.text().strip() == 'text'


@requires_tika
def test_office(mock_osp):

    """
    Should extract text from office files.
    """

    path = mock_osp.add_file(content='text', ftype='docx')
    syllabus = Syllabus(path)

    assert syllabus.text().strip() == 'text'
