

import re

from osp.corpus.models.document import Document
from osp.dates.models.semester import Document_Date_File_Metadata
from datetime import datetime


def ext_file_metadata(id):

    """
    Try to extract created dates from file metadata on PDF and DOCX files.

    Args:
        id (int): The document id.
    """

    doc = Document.get(Document.id==id)
