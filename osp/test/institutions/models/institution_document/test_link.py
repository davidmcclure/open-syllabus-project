

import pytest

from osp.institutions.models import Institution_Document


pytestmark = pytest.mark.usefixtures('db')


def test_link(add_doc, add_institution):

    """
    .link() should link documents -> institutions.
    """

    i1 = add_institution(url='http://d1.edu')
    i2 = add_institution(url='http://d2.edu')
    i3 = add_institution(url='http://d3.edu')

    d1 = add_doc(log=dict(url='http://d1.edu/syllabus.pdf'))
    d2 = add_doc(log=dict(url='http://d2.edu/syllabus.pdf'))
    d3 = add_doc(log=dict(url='http://d3.edu/syllabus.pdf'))

    Institution_Document.link()

    for i, d in [
        (i1, d1),
        (i2, d2),
        (i3, d3),
    ]:

        assert Institution_Document.select().where(
            Institution_Document.institution==i,
            Institution_Document.document==d,
        )


def test_match_subdomains(add_doc, add_institution):

    """
    If the document has a subdomain(s), it should be matched "greedily" against
    the institutions - find the institution with the most shared subdomains.
    """

    i1 = add_institution(url='http://yale.edu')
    i2 = add_institution(url='http://sub1.yale.edu')
    i3 = add_institution(url='http://sub2.sub1.yale.edu')
    i4 = add_institution(url='http://sub3.sub2.sub1.yale.edu')

    d1 = add_doc(log=dict(url='http://yale.edu/syllabus.pdf'))
    d2 = add_doc(log=dict(url='http://sub1.yale.edu/syllabus.pdf'))
    d3 = add_doc(log=dict(url='http://sub2.sub1.yale.edu/syllabus.pdf'))
    d4 = add_doc(log=dict(url='http://sub3.sub2.sub1.yale.edu/syllabus.pdf'))

    Institution_Document.link()

    for i, d in [
        (i1, d1),
        (i2, d2),
        (i3, d3),
        (i4, d4),
    ]:

        assert Institution_Document.select().where(
            Institution_Document.institution==i,
            Institution_Document.document==d,
        )


# simple linking

# if the doc has a subdomain, it should be matched "greedily" against the
# available institutions. Eg, if we have institutions:

# yale.edu
# sub1.yale.edu
# sub2.sub1.yale.edu
# sub3.sub2.sub1.yale.edu

# yale.edu/file -> yale.edu
# sub1.yale.edu/file -> sub1.yale.edu
# sub2.sub1.yale.edu/file -> sub2.sub1.yale.edu
# sub3.sub2.sub1.yale.edu/file -> sub3.sub2.sub1.yale.edu

# likewise with paths

# yale.edu
# yale.edu/path1
# yale.edu/path1/path2
# yale.edu/path1/path2/path3

# yale.edu/file -> yale.edu
# yale.edu/path1/file -> yale.edu/path1
# yale.edu/path1/path2/file -> yale.edu/path1/path2
# yale.edu/path1/path2/path3/file -> yale.edu/path1/path2/path3
