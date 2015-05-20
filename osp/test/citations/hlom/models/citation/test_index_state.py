

from osp.citations.hlom.models.citation import HLOM_Citation
from osp.institutions.models.institution import Institution
from osp.locations.models.doc_inst import Document_Institution


def test_index_state(add_hlom, add_doc):

    """
    HLOM_Citation.index_state() should denormalize state abbrevations from the
    institution associated with the citation.
    """

    t1 = add_hlom()
    t2 = add_hlom()
    t3 = add_hlom()

    s1 = add_doc('syllabus1')
    s2 = add_doc('syllabus2')
    s3 = add_doc('syllabus3')

    c1 = HLOM_Citation.create(document=s1, record=t1)
    c2 = HLOM_Citation.create(document=s2, record=t2)
    c3 = HLOM_Citation.create(document=s3, record=t3)

    AL = Institution.create(metadata={'Institution_State': 'AL'})
    CT = Institution.create(metadata={'Institution_State': 'CT'})
    CA = Institution.create(metadata={'Institution_State': 'CA'})

    Document_Institution.create(document=t1, institution=AL)
    Document_Institution.create(document=t2, institution=CT)
    Document_Institution.create(document=t3, institution=CA)

    HLOM_Citation.index_state()

    c1 = HLOM_Citation.reload(c1)
    c2 = HLOM_Citation.reload(c2)
    c3 = HLOM_Citation.reload(c3)

    assert c1.state == 'AL'
    assert c2.state == 'CT'
    assert c3.state == 'CA'
