

from osp.corpus.corpus import Corpus
from osp.test.utils import segment_range


def test_insert_documents(mock_corpus, Document):

    """
    Corpus.insert_documents() should create a `document` row for each syllabus
    in the corpus.
    """

    # Add 10 segments with 10 files.
    for s in segment_range(0, 10):
        mock_corpus.add_segment(s)
        mock_corpus.add_files(s, 10, prefix=s+'-')

    # Insert document rows.
    corpus = Corpus(mock_corpus.path)
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
