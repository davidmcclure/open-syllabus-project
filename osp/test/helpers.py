

import pytest
import uuid

from osp.corpus.syllabus import Syllabus
from osp.corpus.jobs import ext_text
from osp.corpus.models import Document

from osp.fields.models import Subfield
from osp.fields.models import Subfield_Document
from osp.fields.models import Field

from osp.citations.models import Text
from osp.citations.models import Citation

from osp.institutions.models import Institution


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
        tokens=['one', 'two'],
    ):

        if not text:
            text = add_text()

        if not document:
            document = add_doc()

        return Citation.create(
            text=text,
            document=document,
            tokens=tokens,
        )

    return _citation


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
        field=None,
    ):

        if not field:
            field = Field.create(name='Parent')

        return Subfield.create(
            name=name,
            abbreviations=abbreviations,
            field=field,
        )

    return _subfield


@pytest.fixture()
def add_subfield_document(models, add_subfield, add_doc):

    """
    Link a document -> subfield.

    Returns:
        function
    """

    def _subfield_document(
        subfield=None,
        document=None,
        snippet='field',
        offset=100,
    ):

        if not subfield:
            subfield = add_subfield()

        if not document:
            document = add_doc()

        return Subfield_Document.create(
            subfield=subfield,
            document=document,
            offset=offset,
            snippet=snippet,
        )

    return _subfield_document


@pytest.fixture()
def add_institution(models):

    """
    Create an institution

    Returns:
        function
    """

    def _inst(
        name='Yale University',
        domain=None,
    ):

        if not domain:
            domain = uuid.uuid4()

        return Institution.create(
            name=name,
            domain=domain,
        )

    return _inst
