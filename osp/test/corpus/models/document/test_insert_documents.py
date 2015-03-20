

from osp.corpus.corpus import Corpus
from osp.corpus.models.document import Document
from osp.test.utils import segment_range


def test_insert_documents(models, mock_osp):

    """
    Corpus.insert_documents() should create a `document` row for each syllabus
    in the corpus.
    """

    # 10 segments * 10 files.
    for s in segment_range(0, 10):
        mock_osp.add_segment(s)
        mock_osp.add_files(s, 10, prefix=s+'-')

    # Insert document rows.
    corpus = Corpus(mock_osp.path)
    Document.insert_documents(corpus)

    # Should create 100 rows.
    assert Document.select().count() == 100

    # All 100 paths should have rows.
    for s in segment_range(0, 10):
        for i in range(0, 10):

            # Query for the document path.
            path = s+'/'+s+'-'+str(i)
            query = Document.select().where(Document.path==path)
            assert query.count() == 1
