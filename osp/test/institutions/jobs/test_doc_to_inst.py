

from osp.institutions.models import Institution
from osp.institutions.models import Institution_Document
from osp.institutions.jobs import doc_to_inst


def test_match(add_doc, add_institution):

    """
    When a doc URL matches an institution domain, write a link.
    """

    doc = add_doc(log={
        'url': 'http://yale.edu/syllabus.pdf'
    })

    yale = add_institution(
        name='Yale University',
        domain='yale.edu',
    )

    harvard = add_institution(
        name='Harvard University',
        domain='harvard.edu',
    )

    doc_to_inst(doc.id)

    # Should write a link.
    assert Institution_Document.select().count() == 1

    # Should link the right rows.
    assert Institution_Document.select().where(
        Institution_Document.institution==yale,
        Institution_Document.document==doc,
    )


def test_no_match(add_doc, add_institution):

    """
    When the URL doesn't match an institution, don't write a row.
    """

    doc = add_doc(log={
        'url': 'http://yale.edu/syllabus.pdf'
    })

    harvard = add_institution(
        name='Harvard University',
        domain='harvard.edu',
    )

    doc_to_inst(doc.id)

    # Shouldn't write a link.
    assert Institution_Document.select().count() == 0
