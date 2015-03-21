

import pytest

from osp.corpus.models.document import Document
from osp.citations.hlom.models.record import HLOM_Record
from osp.corpus.jobs.ext_text import ext_text


@pytest.fixture()
def add_hlom(models, mock_hlom):

    """
    Mock an HLOM MARC record, create a `hlom_record` row.

    Returns:
        function
    """

    def _hlom(title='', author=''):

        # Mock a MARC record.
        marc = mock_hlom.add_marc(
            title=title,
            author=author
        )

        # Create a `hlom_record` row.
        return HLOM_Record.create(
            control_number=marc.control_number(),
            record=marc.as_marc()
        )

    return _hlom


@pytest.fixture()
def add_doc(models, mock_osp):

    """
    Mocks a file, create a `document` row, extract text.

    Returns:
        function
    """

    def _doc(content):

        # Mock a file.
        path = mock_osp.add_file(content=content)

        # Create a `document` row.
        document = Document.create(path=path)

        # Extract text.
        text = ext_text(document.id)

        return document

    return _doc
