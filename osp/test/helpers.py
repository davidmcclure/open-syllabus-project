

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


# TODO: Use FactoryBoy?


@pytest.fixture()
def add_doc(mock_osp):

    """
    Mock a file, create a `document` row, extract text.
    """

    def _doc(*args, **kwargs):

        # Write a file.
        path = mock_osp.add_file(*args, **kwargs)
        syllabus = Syllabus(path)

        # Insert the document row.
        document = Document.create(path=syllabus.relative_path())

        # Extract text.
        text = ext_text(document.id)

        return document

    return _doc


@pytest.fixture()
def add_text():

    """
    Create a text.
    """

    def _text(
        corpus='corpus',
        identifier=None,
        title='Title',
        surname='Surname',
        authors=['Author'],
        valid=True,
        display=True,
        **kwargs
    ):

        if not identifier:
            identifier = uuid.uuid4()

        return Text.create(
            corpus=corpus,
            identifier=identifier,
            title=title,
            surname=surname,
            authors=authors,
            valid=valid,
            display=display,
            **kwargs
        )

    return _text


@pytest.fixture()
def add_citation(add_doc, add_text):

    """
    Create a citation.
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
def add_subfield():

    """
    Create a field and subfield.
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
def add_subfield_document(add_subfield, add_doc):

    """
    Link a document -> subfield.
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
def add_institution():

    """
    Create an institution
    """

    def _inst(
        name='Yale University',
        url=None,
        domain=None,
        state='CA',
        country='US',
    ):

        if not url:
            url = uuid.uuid4()

        if not domain:
            domain = uuid.uuid4()

        return Institution.create(
            name=name,
            url=url,
            domain=domain,
            state=state,
            country=country,
        )

    return _inst
