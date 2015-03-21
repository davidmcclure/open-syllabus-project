

from osp.corpus.corpus import Corpus
from osp.corpus.models.document import Document
from osp.test.utils import segment_range


def test_insert_documents(models, mock_osp):

    """
    Corpus.insert_documents() should create a row for each syllabus.
    """

    # 10 segments x 10 files.
    for s in segment_range(10):
        mock_osp.add_segment(s)
        mock_osp.add_files(s, 10, prefix=s+'-')

    # Insert document rows.
    Document.insert_documents()

    # Should create 100 rows.
    assert Document.select().count() == 100

    # All docs should have rows.
    for s in segment_range(10):
        for i in range(10):

            # Query for the document path.
            path = s+'/'+s+'-'+str(i)
            query = Document.select().where(Document.path==path)
            assert query.count() == 1
