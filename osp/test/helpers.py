

import pytest
import uuid

from osp.corpus.syllabus import Syllabus
from osp.corpus.jobs import ext_text
from osp.corpus.models import Document

from osp.fields.models import Field
from osp.fields.models import Subfield

from osp.citations.models import Text
from osp.citations.models import Citation


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

    def _subfield(
        name='Field',
        abbreviations=None,
        parent_name='Field',
    ):

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

    def _text(
        corpus='corpus',
        identifier=None,
        title='Title',
        author=['Author'],
    ):

        if not identifier:
            identifier = uuid.uuid4()

        return Text.create(
            corpus=corpus,
            identifier=identifier,
            title=title,
            author=author,
        )

    return _text


@pytest.fixture()
def add_citation(models, add_doc, add_text):

    """
    Create a citation.

    Returns:
        function
    """

    def _citation(
        text=None,
        document=None,
        tokens=[],
    ):

        if not text:
            text = add_text()

        if not document:
            document = add_doc()

        Citation.create(
            text=text,
            document=document,
            tokens=tokens,
        )

    return _citation
