

import pytest

from osp.corpus.models.document import Document
from osp.corpus.jobs.ext_text import ext_text
from osp.citations.hlom.models.record import HLOM_Record
from osp.citations.hlom.models.citation import HLOM_Citation
from osp.citations.hlom.jobs.query import query
from pymarc import Record, Field


def get_hlom(number, title, author):

    """
    Insert a HLOM record row.

    Args:
        number (str): The control number.
        title (str): The title.
        author (str): The author.

    Returns:
        pymarc.Record
    """

    marc = Record()

    f001 = Field(
        tag='001',
        indicators=['0', '1'],
        subfields=['a', number]
    )

    f100 = Field(
        tag='100',
        indicators=['0', '1'],
        subfields=['a', author]
    )

    f245 = Field(
        tag='245',
        indicators=['0', '1'],
        subfields=['a', title]
    )

    marc.add_field(f001)
    marc.add_field(f100)
    marc.add_field(f245)

    return HLOM_Record.create(
        control_number=number,
        record=marc.as_marc()
    )


@pytest.fixture()
def doc(models, mock_osp):

    """
    Mocks a file, create a document row, and extract text.

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


def test_matches(doc, corpus_index):

    """
    When OSP documents match the query, write link rows.
    """

    d1 = doc('War and Peace, Leo Tolstoy 1')
    d2 = doc('War and Peace, Leo Tolstoy 2')
    d3 = doc('War and Peace, Leo Tolstoy 3')
    d4 = doc('Anna Karenina, Leo Tolstoy 1')
    d5 = doc('Anna Karenina, Leo Tolstoy 2')

    corpus_index.index()

    hlom = get_hlom('1', 'War and Peace', 'Leo Tolstoy')
    query(hlom.id)

    # Should write 3 citation links.
    assert HLOM_Citation.select().count() == 3

    # Should match the right documents.
    for doc in [d1, d2, d3]:

        assert HLOM_Citation.select().where(
            HLOM_Citation.document==doc,
            HLOM_Citation.record==hlom
        )


def test_no_matches(doc, corpus_index):

    """
    When no documents match, don't write any rows.
    """

    doc('War and Peace, Leo Tolstoy')
    corpus_index.index()

    hlom = get_hlom('1', 'Master and Man', 'Leo Tolstoy')
    query(hlom.id)

    # Shouldn't write any rows.
    assert HLOM_Citation.select().count() == 0
