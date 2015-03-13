

from osp.corpus.models.document import Document
from osp.dates.models.file_metadata import Document_Date_File_Metadata
from osp.dates.jobs.ext_file_metadata import ext_file_metadata
from datetime import datetime


def test_pdf(models, mock_corpus):

    """
    ext_file_metadata() should extract the created date from a PDF.
    """

    now = datetime.now()

    # Create a document.
    path = mock_corpus.add_file(ftype='pdf')
    document = Document.create(path=path)

    # Extract the date.
    ext_file_metadata(document.id)

    # Pop out the new row.
    row = Document_Date_File_Metadata.get(
        Document_Date_File_Metadata.document==document
    )

    # Created within a second of now.
    assert abs(row.date - now).seconds <= 1


def test_docx(models, mock_corpus):

    """
    ext_file_metadata() should extract the created date from a DOCX.
    """

    now = datetime.now()

    # Create a document.
    path = mock_corpus.add_file(ftype='docx')
    document = Document.create(path=path)

    # Extract the date.
    ext_file_metadata(document.id)

    # Pop out the new row.
    row = Document_Date_File_Metadata.get(
        Document_Date_File_Metadata.document==document
    )

    # Created within a second of now.
    assert abs(row.date - now).seconds <= 1
