

import pytest

from osp.institutions.models import Institution_Document
from osp.institutions.jobs import DocToInst


pytestmark = pytest.mark.usefixtures('db')


def test_match(add_doc, add_institution):

    """
    When a document URL matches an institution URL, write a link.
    """

    i1 = add_institution(url='http://d1.edu')
    i2 = add_institution(url='http://d2.edu')
    i3 = add_institution(url='http://d3.edu')

    d1 = add_doc(log=dict(url='http://d1.edu/syllabus.pdf'))
    d2 = add_doc(log=dict(url='http://d2.edu/syllabus.pdf'))
    d3 = add_doc(log=dict(url='http://d3.edu/syllabus.pdf'))

    DocToInst.run()

    for i, d in [
        (i1, d1),
        (i2, d2),
        (i3, d3),
    ]:

        assert Institution_Document.select().where(
            Institution_Document.document==d,
            Institution_Document.institution==i,
        )
