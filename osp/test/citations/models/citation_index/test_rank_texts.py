

import pytest

from osp.citations.models import Citation_Index
from osp.institutions.models import Institution_Document
from wordfreq import word_frequency


pytestmark = pytest.mark.usefixtures('db', 'es')


def test_unfiltered(add_text, add_citation):

    """
    When no filters are provided, return total counts.
    """

    t1 = add_text()
    t2 = add_text()
    t3 = add_text()

    for i in range(3):
        add_citation(t1)

    for i in range(2):
        add_citation(t2)

    for i in range(1):
        add_citation(t3)

    Citation_Index.es_insert()

    ranks = Citation_Index.rank_texts()

    assert ranks == {
        str(t1.id): 3,
        str(t2.id): 2,
        str(t3.id): 1,
    }


def test_filter_corpus(add_text, add_citation):

    """
    Filter on corpus as a keyword value.
    """

    t1 = add_text(corpus='corpus1')
    t2 = add_text(corpus='corpus1')
    t3 = add_text(corpus='corpus2')

    for i in range(3):
        add_citation(t1)

    for i in range(2):
        add_citation(t2)

    for i in range(1):
        add_citation(t3)

    Citation_Index.es_insert()

    ranks = Citation_Index.rank_texts(dict(
        corpus='corpus1'
    ))

    assert ranks == {
        str(t1.id): 3,
        str(t2.id): 2,
    }


def test_filter_subfield(
    add_text,
    add_citation,
    add_subfield,
    add_subfield_document,
):

    """
    Filter by subfield.
    """

    t1 = add_text()
    t2 = add_text()
    t3 = add_text()

    sf1 = add_subfield()
    sf2 = add_subfield()

    for i in range(3):
        c = add_citation(text=t1)
        add_subfield_document(subfield=sf1, document=c.document)

    for i in range(2):
        c = add_citation(text=t2)
        add_subfield_document(subfield=sf1, document=c.document)

    for i in range(1):
        c = add_citation(text=t3)
        add_subfield_document(subfield=sf2, document=c.document)

    Citation_Index.es_insert()

    ranks = Citation_Index.rank_texts(dict(
        subfield_id=sf1.id
    ))

    assert ranks == {
        str(t1.id): 3,
        str(t2.id): 2,
    }


def test_filter_field(
    add_text,
    add_citation,
    add_subfield,
    add_subfield_document,
):

    """
    Filter by field.
    """

    t1 = add_text()
    t2 = add_text()
    t3 = add_text()

    sf1 = add_subfield()
    sf2 = add_subfield()

    for i in range(3):
        c = add_citation(text=t1)
        add_subfield_document(subfield=sf1, document=c.document)

    for i in range(2):
        c = add_citation(text=t2)
        add_subfield_document(subfield=sf1, document=c.document)

    for i in range(1):
        c = add_citation(text=t3)
        add_subfield_document(subfield=sf2, document=c.document)

    Citation_Index.es_insert()

    ranks = Citation_Index.rank_texts(dict(
        field_id=sf1.field.id
    ))

    assert ranks == {
        str(t1.id): 3,
        str(t2.id): 2,
    }


def test_filter_institution(add_text, add_citation, add_institution):

    """
    Filter by institution.
    """

    t1 = add_text()
    t2 = add_text()
    t3 = add_text()

    i1 = add_institution()
    i2 = add_institution()

    for i in range(3):
        c = add_citation(text=t1)
        Institution_Document.create(institution=i1, document=c.document)

    for i in range(2):
        c = add_citation(text=t2)
        Institution_Document.create(institution=i1, document=c.document)

    for i in range(1):
        c = add_citation(text=t3)
        Institution_Document.create(institution=i2, document=c.document)

    Citation_Index.es_insert()

    ranks = Citation_Index.rank_texts(dict(
        institution_id=i1.id
    ))

    assert ranks == {
        str(t1.id): 3,
        str(t2.id): 2,
    }


def test_filter_state(add_text, add_citation, add_institution):

    """
    Filter on state as a keyword value.
    """

    t1 = add_text()
    t2 = add_text()
    t3 = add_text()

    i1 = add_institution(state='AL')
    i2 = add_institution(state='CA')

    for i in range(3):
        c = add_citation(text=t1)
        Institution_Document.create(institution=i1, document=c.document)

    for i in range(2):
        c = add_citation(text=t2)
        Institution_Document.create(institution=i1, document=c.document)

    for i in range(1):
        c = add_citation(text=t3)
        Institution_Document.create(institution=i2, document=c.document)

    Citation_Index.es_insert()

    ranks = Citation_Index.rank_texts(dict(
        state='AL'
    ))

    assert ranks == {
        str(t1.id): 3,
        str(t2.id): 2,
    }


def test_filter_country(add_text, add_citation, add_institution):

    """
    Filter on country as a keyword value.
    """

    t1 = add_text()
    t2 = add_text()
    t3 = add_text()

    i1 = add_institution(country='USA')
    i2 = add_institution(country='CAN')

    for i in range(3):
        c = add_citation(text=t1)
        Institution_Document.create(institution=i1, document=c.document)

    for i in range(2):
        c = add_citation(text=t2)
        Institution_Document.create(institution=i1, document=c.document)

    for i in range(1):
        c = add_citation(text=t3)
        Institution_Document.create(institution=i2, document=c.document)

    Citation_Index.es_insert()

    ranks = Citation_Index.rank_texts(dict(
        country='USA'
    ))

    assert ranks == {
        str(t1.id): 3,
        str(t2.id): 2,
    }


def test_filter_multiple_values(add_text, add_citation):

    """
    When a list of values is provided for a filter key, match citations that
    include _any_ of the provided values for the key.
    """

    t1 = add_text(corpus='corpus1')
    t2 = add_text(corpus='corpus2')
    t3 = add_text(corpus='corpus3')

    for i in range(3):
        add_citation(t1)

    for i in range(2):
        add_citation(t2)

    for i in range(1):
        add_citation(t3)

    Citation_Index.es_insert()

    ranks = Citation_Index.rank_texts(dict(
        corpus=['corpus1', 'corpus3']
    ))

    # Count both `corpus1` and `corpus3` citations.
    assert ranks == {
        str(t1.id): 3,
        str(t3.id): 1,
    }


def test_filter_min_freq(add_text, add_citation):

    """
    If a `min_freq` argument is provided, just count citations with a min_freq
    _below_ the passed value.
    """

    text = add_text()

    add_citation(text=text, tokens=['one'])
    add_citation(text=text, tokens=['two'])
    add_citation(text=text, tokens=['three'])
    add_citation(text=text, tokens=['four'])
    add_citation(text=text, tokens=['five'])

    Citation_Index.es_insert()

    for token, count in [
        ('one', 5),
        ('two', 4),
        ('three', 3),
        ('four', 2),
        ('five', 1),
    ]:

        ranks = Citation_Index.rank_texts(
            min_freq=word_frequency(token, 'en')*1e6
        )

        assert ranks == {
            str(text.id): count
        }


@pytest.mark.parametrize('empty', [
    None,
    [],
])
def test_ignore_filters_with_empty_values(empty, add_text, add_citation):

    """
    Ignore filters with empty values.
    """

    t1 = add_text(corpus='corpus1')
    t2 = add_text(corpus='corpus2')
    t3 = add_text(corpus='corpus3')

    for i in range(3):
        add_citation(t1)

    for i in range(2):
        add_citation(t2)

    for i in range(1):
        add_citation(t3)

    Citation_Index.es_insert()

    ranks = Citation_Index.rank_texts(dict(
        corpus=empty
    ))

    assert ranks == {
        str(t1.id): 3,
        str(t2.id): 2,
        str(t3.id): 1,
    }
