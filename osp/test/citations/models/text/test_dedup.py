

import pytest

from osp.citations.models import Text


pytestmark = pytest.mark.usefixtures('db', 'redis')


def test_dedup(add_text, add_citation):

    """
    Text.dedup() should:

        - For texts that aren't duplicates, display=True and duplicate=False.

        - For sets of duplicate texts, the _first_  text (in terms of id order)
          should have display=True, and all should have duplicate=False.
    """

    t1 = add_text(title='one', surname='two')
    t2 = add_text(title='one', surname='two')

    t3 = add_text(title='three', surname='four')
    t4 = add_text(title='three', surname='four')

    t5 = add_text(title='five', surname='six')

    add_citation(text=t1)
    add_citation(text=t2)
    add_citation(text=t3)
    add_citation(text=t4)
    add_citation(text=t5)

    Text.dedup()

    t1 = Text.get(Text.id==t1.id)
    t2 = Text.get(Text.id==t2.id)
    t3 = Text.get(Text.id==t3.id)
    t4 = Text.get(Text.id==t4.id)
    t5 = Text.get(Text.id==t5.id)

    assert t1.display == True
    assert t1.duplicate == True

    assert t2.display == False
    assert t2.duplicate == True

    assert t3.display == True
    assert t3.duplicate == True

    assert t4.display == False
    assert t4.duplicate == True

    assert t5.display == True
    assert t5.duplicate == False
