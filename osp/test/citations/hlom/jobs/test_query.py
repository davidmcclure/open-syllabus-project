

import pytest

from osp.corpus.models.document import Document
from osp.corpus.jobs.ext_text import ext_text
from osp.citations.hlom.models.record import HLOM_Record
from osp.citations.hlom.models.citation import HLOM_Citation
from osp.citations.hlom.jobs.query import query


@pytest.fixture()
def hlom(models, mock_hlom):

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
def doc(models, mock_osp):

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


def test_matches(corpus_index, mock_hlom, doc, hlom):

    """
    When OSP documents match the query, write link rows.
    """

    d1 = doc('War and Peace, Leo Tolstoy 1')
    d2 = doc('War and Peace, Leo Tolstoy 2')
    d3 = doc('War and Peace, Leo Tolstoy 3')
    d4 = doc('Anna Karenina, Leo Tolstoy 1')
    d5 = doc('Anna Karenina, Leo Tolstoy 2')

    corpus_index.index()

    record = hlom('War and Peace', 'Leo Tolstoy')
    query(record.id)

    # Should write 3 citation links.
    assert HLOM_Citation.select().count() == 3

    # Should match the right documents.
    for doc in [d1, d2, d3]:

        assert HLOM_Citation.select().where(
            HLOM_Citation.document==doc,
            HLOM_Citation.record==record
        )


def test_no_matches(corpus_index, doc, hlom):

    """
    When no documents match, don't write any rows.
    """

    doc('War and Peace, Leo Tolstoy')
    corpus_index.index()

    record = hlom('Master and Man', 'Leo Tolstoy')
    query(record.id)

    # Shouldn't write any rows.
    assert HLOM_Citation.select().count() == 0
