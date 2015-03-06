

from osp.corpus.syllabus import Syllabus


def test_syllabus(Document, config, mock_corpus):

    """
    Document#syllabus should provide a Syllabus instance bound to the file
    referenced by the document row.
    """

    config.config.update_w_merge({
        'osp': {
            'corpus': mock_corpus.path
        }
    })

    path = mock_corpus.add_file('000', name='123')
    doc = Document(path='000/123')

    assert isinstance(doc.syllabus, Syllabus)
    assert doc.syllabus.path == path
