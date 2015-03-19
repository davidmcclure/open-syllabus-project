

import pytest

from osp.corpus.models.document import Document
from osp.dates.models.file_metadata import Document_Date_File_Metadata
from osp.dates.jobs.ext_file_metadata import ext_file_metadata
from datetime import datetime


@pytest.fixture()
def ext(models, mock_corpus):

    """
    Provide a function that mocks a file and returns a document instance bound
    to the new path.

    Returns:
        function: A helper that mocks a file, runs the job, and returns the
        new `document_date_file_metadata` row.
    """

    def _ext(ftype):

        # Create a document.
        path = mock_corpus.add_file(ftype=ftype)
        document = Document.create(path=path)

        # Extract the date.
        ext_file_metadata(document.id)

        # Pop out the new row.
        return (
            Document_Date_File_Metadata
            .select()
            .where(Document_Date_File_Metadata.document==document)
            .first()
        )

    return _ext


def test_pdf(ext):

    """
    ext_file_metadata() should extract the created date from a PDF.
    """

    now = datetime.now()
    row = ext('pdf')

    # Created within a second of now.
    assert abs(row.date - now).seconds <= 10


def test_docx(ext):

    """
    ext_file_metadata() should extract the created date from a DOCX.
    """

    now = datetime.now()
    row = ext('docx')

    # Created within a second of now.
    assert abs(row.date - now).seconds <= 10


def test_ignore_plaintext(ext):

    """
    ext_file_metadata() should ignore plaintext files.
    """

    row = ext('plain')
    assert row == None


def test_ignore_html(ext):

    """
    ext_file_metadata() should ignore HTML files.
    """

    row = ext('html')
    assert row == None
