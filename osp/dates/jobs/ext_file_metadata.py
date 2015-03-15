

import re

from osp.corpus.models.document import Document
from osp.dates.models.file_metadata import Document_Date_File_Metadata
from datetime import datetime


def ext_file_metadata(doc_id):

    """
    Try to extract a created date from PDF and DOCX file metadata.

    Args:
        id (int): The document id.
    """

    doc = Document.get(Document.id==doc_id)
    date = doc.syllabus.created_date

    if date:

        return Document_Date_File_Metadata.create(
            document=doc,
            date=date
        )
