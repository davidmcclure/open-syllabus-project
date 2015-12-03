

import pytest

from osp.corpus.syllabus import Syllabus
from osp.corpus.models.document import Document
from osp.corpus.jobs.ext_text import ext_text


@pytest.fixture()
def add_doc(models, mock_osp):

    """
    Mocks a file, create a `document` row, extract text.

    Returns:
        function
    """

    def _doc(content='content'):

        # Write a file.
        path = mock_osp.add_file(content=content)
        syllabus = Syllabus(path)

        # Insert the document row.
        document = Document.create(path=syllabus.relative_path)

        # Extract text.
        text = ext_text(document.id)

        return document

    return _doc
