

import pytest

from osp.citations.validator import Validator


pytestmark = pytest.mark.usefixtures('db')


def test_reject_duplicates(add_text, add_citation, add_doc):

    """
    If a (text hash, doc id) citation has aleady been seen by the validator,
    invalidate the duplicate.
    """

    v = Validator()

    # Duplicate texts.
    t1 = add_text(surname='one', title='two')
    t2 = add_text(surname='one', title='two')

    d1 = add_doc()
    d2 = add_doc()

    # See t1 first.
    assert v.validate(add_citation(text=t1, document=d1)) == True

    # Block t2 on other docs.
    assert v.validate(add_citation(text=t2, document=d1)) == False
    assert v.validate(add_citation(text=t2, document=d2)) == False


def test_reject_title_same_as_author(add_text, add_citation):

    """
    Reject citations for which the title tokens are the same as the author
    tokens.
    """

    v = Validator()

    text = add_text(surname='plato', title='plato')

    assert v.validate(add_citation(text=text)) == False


def test_reject_blacklisted_titles(add_text, add_citation):

    """
    Reject citations for which the text has a title that consists of a single
    blacklisted token.
    """

    v = Validator()

    t1 = add_text(surname='napoleon', title='letter home')
    t2 = add_text(surname='napoleon', title='letter')

    # Multi-token title passes.
    assert v.validate(add_citation(text=t1)) == True

    # Single-token fails.
    assert v.validate(add_citation(text=t2)) == False


def test_reject_fuzzy_tokens(add_text, add_citation):

    """
    Reject citations for which the "fuzz" score is above a given threshold.
    """

    t1 = add_text(surname='one')
    t2 = add_text(surname='two')
    t3 = add_text(surname='three')
    t4 = add_text(surname='four')
    t5 = add_text(surname='five')

    c1 = add_citation(text=t1, tokens=['one'])
    c2 = add_citation(text=t2, tokens=['two'])
    c3 = add_citation(text=t3, tokens=['three'])
    c4 = add_citation(text=t4, tokens=['four'])
    c5 = add_citation(text=t5, tokens=['five'])

    v = Validator(max_fuzz=c3.fuzz)

    assert v.validate(c1) == False
    assert v.validate(c2) == False
    assert v.validate(c3) == True
    assert v.validate(c4) == True
    assert v.validate(c5) == True
