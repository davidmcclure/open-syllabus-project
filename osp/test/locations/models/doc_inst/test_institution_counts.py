

from osp.institutions.models.institution import Institution
from osp.locations.models.doc_inst import Document_Institution
from osp.corpus.models.document import Document


def test_institution_counts(models):

    """
    Document_Institution.institution_counts() should provide syllabus counts
    for each institution id.
    """

    i1 = Institution.create()
    i2 = Institution.create()
    i3 = Institution.create()

    d1 = Document.create(path='d1')
    d2 = Document.create(path='d2')
    d3 = Document.create(path='d3')
    d4 = Document.create(path='d4')
    d5 = Document.create(path='d5')
    d6 = Document.create(path='d6')

    # 1 document for institution 1.
    Document_Institution.create(institution=i1, document=d1)

    # 2 documents for institution 2.
    Document_Institution.create(institution=i2, document=d2)
    Document_Institution.create(institution=i2, document=d3)

    # 3 documents for institution 3.
    Document_Institution.create(institution=i3, document=d4)
    Document_Institution.create(institution=i3, document=d5)
    Document_Institution.create(institution=i3, document=d6)

    assert Document_Institution.institution_counts() == {
        d1.id: 1,
        d2.id: 2,
        d3.id: 3,
    }
