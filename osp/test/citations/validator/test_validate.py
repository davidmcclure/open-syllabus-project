

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
