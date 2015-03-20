

from osp.corpus.models.document import Document
from osp.corpus.jobs.ext_text import ext_text


def test_matches(models, mock_osp, corpus_index):

    """
    When OSP documents match the query, write link rows.
    """

    pass

    #p1 = mock_osp.add_file(content='War and Peace, Leo Tolstoy')
    #p2 = mock_osp.add_file(content='War and Peace, Leo Tolstoy')
    #p3 = mock_osp.add_file(content='War and Peace, Leo Tolstoy')
    #p4 = mock_osp.add_file(content='Anna Karenina, Leo Tolstoy')
    #p5 = mock_osp.add_file(content='Anna Karenina, Leo Tolstoy')

    #d1 = Document.create(path=p1)
    #d2 = Document.create(path=p2)
    #d3 = Document.create(path=p3)
    #d4 = Document.create(path=p4)
    #d5 = Document.create(path=p5)

    #t1 = ext_text(d1.id)
    #t2 = ext_text(d2.id)
    #t3 = ext_text(d3.id)
    #t4 = ext_text(d4.id)
    #t5 = ext_text(d5.id)

    #corpus_index.index()

    ## add hlom_record row for WP
    ## query()
    ## check for hlom_citation links
