

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

    # First pairing validates.
    assert v.validate(add_citation(text=t1, document=d1)) == True
    assert v.validate(add_citation(text=t2, document=d1)) == False


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

    t1 = add_text(surname='napoleon', title='letters home')
    t2 = add_text(surname='napoleon', title='letters')

    # Multi-token title passes.
    assert v.validate(add_citation(text=t1)) == True

    # Single-token fails.
    assert v.validate(add_citation(text=t2)) == False
