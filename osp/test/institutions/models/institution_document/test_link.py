

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


def test_match_paths(add_doc, add_institution):

    """
    If the document has a path, it should be matched "greedily" against
    the institutions - find the institution with the longest shared path.
    """

    i1 = add_institution(url='http://yale.edu')
    i2 = add_institution(url='http://yale.edu/p1')
    i3 = add_institution(url='http://yale.edu/p1/p2')
    i4 = add_institution(url='http://yale.edu/p1/p2/p3')

    d1 = add_doc(log=dict(url='http://yale.edu/syllabus.pdf'))
    d2 = add_doc(log=dict(url='http://yale.edu/p1/syllabus.pdf'))
    d3 = add_doc(log=dict(url='http://yale.edu/p1/p2/syllabus.pdf'))
    d4 = add_doc(log=dict(url='http://yale.edu/p1/p2/p3/syllabus.pdf'))

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
