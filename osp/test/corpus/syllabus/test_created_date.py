

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

    # Created date should be now.
    assert abs(syllabus.created_date - now).seconds <= 1


def test_docx(mock_corpus):

    """
    Syllabus#created_date should extract the created date from DOCs.
    """

    pass
