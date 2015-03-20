

from osp.corpus.models.document import Document
from osp.corpus.jobs.ext_text import ext_text
from osp.citations.hlom.models.record import HLOM_Record
from osp.citations.hlom.jobs.query import query
from pymarc import Record, Field


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

    marc = Record()

    control = Field(
        tag='001',
        indicators=['0', '1'],
        subfields=['a', '1']
    )

    title = Field(
        tag='245',
        indicators=['0', '1'],
        subfields=['a', 'War and Peace']
    )

    author = Field(
        tag='100',
        indicators=['0', '1'],
        subfields=['a', 'Leo Tolstoy']
    )

    marc.add_field(control)
    marc.add_field(title)
    marc.add_field(author)

    record = HLOM_Record.create(
        control_number='1',
        record=marc.as_marc()
    )

    #query(record.id)

    # add hlom_record row for WP
    # query()
    # check for hlom_citation links
