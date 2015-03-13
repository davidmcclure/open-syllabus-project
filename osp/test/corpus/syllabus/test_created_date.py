

from osp.corpus.syllabus import Syllabus
from datetime import datetime
from PyPDF2 import PdfFileMerger


def test_pdf(mock_corpus):

    """
    Syllabus#created_date should extract the created date from PDFs.
    """

    now = datetime.now()

    path = mock_corpus.add_file(ftype='pdf')
    syllabus = Syllabus(path)

    # Created within a second of now.
    assert abs(syllabus.created_date - now).seconds <= 1


def test_docx(mock_corpus):

    """
    Syllabus#created_date should extract the created date from DOCs.
    """

    now = datetime.now()

    path = mock_corpus.add_file(ftype='docx')
    syllabus = Syllabus(path)

    # Created within a second of now.
    assert abs(syllabus.created_date - now).seconds <= 1


def test_text(mock_corpus):

    """
    If the file isn't a PDF or DOCX, return None.
    """

    path = mock_corpus.add_file(ftype='plain')
    plain = Syllabus(path)

    assert plain.created_date == None

    path = mock_corpus.add_file(ftype='html')
    html = Syllabus(path)

    assert html.created_date == None
