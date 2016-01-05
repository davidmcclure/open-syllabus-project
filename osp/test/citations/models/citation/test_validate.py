

import pytest

from osp.citations.models import Citation


pytestmark = pytest.mark.usefixtures('db')


def test_no_subfield(add_citation, add_text):

    """
    Citation.validete() should write `valid` flags for each row.
    """

    # Valid (title != author).
    c1 = add_citation(text=add_text(surname='one', title='two'))
    c2 = add_citation(text=add_text(surname='three', title='four'))

    # Invalid (title == author).
    c3 = add_citation(text=add_text(surname='five', title='five'))
    c4 = add_citation(text=add_text(surname='six', title='six'))

    Citation.validate()

    for c in [c1, c2]:
        assert Citation.select().where(
            Citation.id==c.id,
            Citation.valid==True,
        )

    for c in [c3, c4]:
        assert Citation.select().where(
            Citation.id==c.id,
            Citation.valid==False,
        )
