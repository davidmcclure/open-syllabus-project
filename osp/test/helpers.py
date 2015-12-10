

import pytest
import uuid

from osp.corpus.syllabus import Syllabus
from osp.corpus.jobs import ext_text
from osp.corpus.models import Document
from osp.citations.models import Text
from osp.fields.models import Field
from osp.fields.models import Subfield


@pytest.fixture()
def add_doc(models, mock_osp):

    """
    Mocks a file, create a `document` row, extract text.

    Returns:
        function
    """

    def _doc(*args, **kwargs):

        # Write a file.
        path = mock_osp.add_file(*args, **kwargs)
        syllabus = Syllabus(path)

        # Insert the document row.
        document = Document.create(path=syllabus.relative_path)

        # Extract text.
        text = ext_text(document.id)

        return document

    return _doc


@pytest.fixture()
def add_subfield(models):

    """
    Create a field and subfield.

    Returns:
        function
    """

    def _subfield(name='Field', abbreviations=None, parent_name='Field'):

        field = Field.create(name=parent_name)

        return Subfield.create(
            name=name,
            abbreviations=abbreviations,
            field=field,
        )

    return _subfield


@pytest.fixture()
def add_text(models):

    """
    Create a text.

    Returns:
        function
    """

    def _text(title='Title', author='Author', identifier=None):

        if not identifier:
            identifier = uuid.uuid4()

        return Text.create(
            identifier=identifier,
            title=title,
            author=author,
        )

    return _text
