

from osp.corpus.models.document import Document
from osp.corpus.jobs.ext_text import ext_text
from osp.citations.hlom.models.record import HLOM_Record
from osp.citations.hlom.models.citation import HLOM_Citation
from osp.citations.hlom.jobs.query import query
from pymarc import Record, Field


def get_marc(number, title, author):

    """
    Create a MARC record.

    Args:
        number (str): The control number.
        title (str): The title.
        author (str): The author.

    Returns:
        pymarc.Record
    """

    record = Record()

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

    record.add_field(f001)
    record.add_field(f100)
    record.add_field(f245)

    return record


def test_matches(models, mock_osp, corpus_index):

    """
    When OSP documents match the query, write link rows.
    """

    p1 = mock_osp.add_file(content='War and Peace, Leo Tolstoy 1')
    p2 = mock_osp.add_file(content='War and Peace, Leo Tolstoy 2')
    p3 = mock_osp.add_file(content='War and Peace, Leo Tolstoy 3')
    p4 = mock_osp.add_file(content='Anna Karenina, Leo Tolstoy 1')
    p5 = mock_osp.add_file(content='Anna Karenina, Leo Tolstoy 2')

    d1 = Document.create(path=p1)
    d2 = Document.create(path=p2)
    d3 = Document.create(path=p3)
    d4 = Document.create(path=p4)
    d5 = Document.create(path=p5)

    t1 = ext_text(d1.id)
    t2 = ext_text(d2.id)
    t3 = ext_text(d3.id)
    t4 = ext_text(d4.id)
    t5 = ext_text(d5.id)

    corpus_index.index()

    marc = get_marc('1', 'War and Peace', 'Leo Tolstoy')

    record = HLOM_Record.create(
        control_number='1',
        record=marc.as_marc()
    )

    query(record.id)

    assert HLOM_Citation.select().count() == 3

    for doc in [d1, d2, d3]:

        assert HLOM_Citation.select().where(
            HLOM_Citation.document==doc,
            HLOM_Citation.record==record
        )
