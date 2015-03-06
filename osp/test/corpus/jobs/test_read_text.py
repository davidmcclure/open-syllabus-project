

from osp.corpus.jobs.read_text import read_text


def test_text_extraction_succeeds(Document, Document_Text, mock_corpus):

    """
    read_text() should extract text for a document and write the result into
    the `document_text` table.
    """

    # Add a file, create a document row.
    path = mock_corpus.add_file(content='text')
    document = Document.create(path=path)

    read_text(document.id)
