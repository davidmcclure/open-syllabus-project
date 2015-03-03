

from osp.corpus.corpus import Corpus
from osp.corpus.utils import int_to_dir


def test_insert_documents(mock_corpus, Document):

    """
    Corpus.insert_documents() should create a `document` row for each syllabus
    in the corpus.
    """

    # Add 10 segments.
    mock_corpus.add_segments(s1=0, s2=10)

    # Add 10 files per segment.
    for i in range(0, 10):
        segment = int_to_dir(i)
        mock_corpus.add_files(segment, 10, prefix=segment+'-')

    # Insert document rows.
    corpus = Corpus(mock_corpus.path)
    Document.insert_documents(corpus)

    # Query for the new rows.
    query = Document.select().order_by(Document.id)

    # Should create 100 rows.
    assert query.count() == 100
